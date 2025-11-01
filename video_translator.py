import argparse
import json
import os
import subprocess
from typing import Literal
import whisper

from subtitles import Subtitles


class VideoTranslator:
    def __init__(self, video_path):
        self.video_path = video_path
        self.whisper_model = whisper.load_model("turbo")

    def convert_video_to_audio(self, video_path: str) -> str:
        audio_path = f"{video_path}.wav"
        result = subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-q:a",
                "0",
                "-map",
                "a",
                "-y",
                audio_path,
                "-v",
                "quiet",
            ]
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to convert video to audio: {result.stderr}")
        return audio_path

    def insert_subtitles_to_video(self, video_path: str, subtitles_path: str) -> str:
        output_video_path = f"{subtitles_path}.mp4"
        result = subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-vf",
                f"subtitles={subtitles_path}",
                "-c:v",
                "libx264",
                "-c:a",
                "copy",
                "-y",
                output_video_path,
                "-v",
                "quiet",
            ]
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to insert subtitles to video: {result.stderr}")
        return output_video_path

    def generate_subtitles(
        self, video_path: str, translation_language: str | None = None
    ) -> Subtitles:
        subtitles: Subtitles = Subtitles()

        audio_path = self.convert_video_to_audio(video_path)
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(
            audio, n_mels=self.whisper_model.dims.n_mels
        ).to(self.whisper_model.device)
        _, probs = self.whisper_model.detect_language(mel)
        subtitles["original_language"] = max(probs, key=probs.get)

        result = self.whisper_model.transcribe(audio_path)
        subtitles["subtitles"] = [
            {
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"],
            }
            for segment in result["segments"]
        ]

        if translation_language:
            subtitles["language"] = translation_language
        else:
            subtitles["language"] = subtitles["original_language"]

        subtitle_path = self.save_subtitles(
            subtitles,
            f"{video_path}_sub_{subtitles['language']}.srt",
        )
        self.insert_subtitles_to_video(video_path, subtitle_path)

        os.remove(audio_path)
        os.remove(subtitle_path)

        return subtitles

    def seconds_to_srt_time(self, seconds: float) -> str:
        total_seconds = int(seconds)
        milliseconds = int((seconds - total_seconds) * 1000)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def save_subtitles(
        self,
        subtitles: Subtitles,
        output_path: str,
        format: Literal["srt", "json"] = None,
    ) -> None:
        if format is None:
            if output_path.endswith(".srt"):
                format = "srt"
            elif output_path.endswith(".json"):
                format = "json"
            else:
                raise ValueError("Output path must end with .srt or .json")

        if format == "srt":
            with open(output_path, "w") as f:
                for index, subtitle in enumerate(subtitles["subtitles"]):
                    f.write(f"{index + 1}\n")
                    f.write(
                        f"{self.seconds_to_srt_time(subtitle['start'])} --> {self.seconds_to_srt_time(subtitle['end'])}\n"
                    )
                    f.write(f"{subtitle['text']}\n")
                    f.write("\n")

        elif format == "json":
            with open(output_path, "w") as f:
                json.dump(subtitles, f, indent=4)

        return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video_path", type=str, required=True, help="Path to the video file"
    )
    parser.add_argument(
        "--language", type=str, required=True, help="Language to translate to"
    )
    parser.add_argument(
        "--output_path", type=str, required=True, help="Path to the output file"
    )
    args = parser.parse_args()
    video_translator = VideoTranslator(args.video_path)
    subtitles = video_translator.generate_subtitles(args.video_path, args.language)
    print(subtitles)
    video_translator.save_subtitles(subtitles, args.output_path)
