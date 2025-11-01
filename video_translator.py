import argparse
import json
import os
import subprocess
from dotenv import load_dotenv
import whisper

from services.openai import OpenAIService
from services.subtitles import Subtitles
import utils


class VideoTranslator:
    def __init__(self, video_path: str, context: str = None):
        load_dotenv()
        self.video_path = video_path
        self.video_name, self.video_extension = utils.split_file_name(video_path)
        self.context = context
        self.whisper_model = whisper.load_model("base")
        self.subtitles = Subtitles()
        self.subtitle_paths: list[str] = []
        self.audio_path: str | None = None
        self.openai_client: OpenAIService = OpenAIService.deepseek_client(
            os.getenv("DEEPSEEK_API_KEY")
        )

    def convert_video_to_audio(self):
        audio_path = f"{self.video_name}.wav"
        result = subprocess.run(
            [
                "ffmpeg",
                "-i",
                self.video_path,
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
        self.audio_path = audio_path

    def insert_subtitles_to_video(self) -> str:
        ffmpeg_subtitles_args = []
        base_margin = 5
        margin_increment = 10  # Margin between language

        font_size = 12 if len(self.subtitles.languages) > 1 else 18

        for index, subtitle_path in enumerate(self.subtitle_paths):
            margin_v = base_margin + (index * margin_increment)
            filter_color = (
                "PrimaryColour=&HFFFFFF,OutlineColour=&H000000"
                if index % 2 == 0
                else "PrimaryColour=&H00FFFF,OutlineColour=&H000000"
            )
            filter_arg = f"subtitles={subtitle_path}:force_style='Alignment=2,Fontsize={font_size},MarginV={margin_v},{filter_color}'"
            ffmpeg_subtitles_args.append(filter_arg)

        ffmpeg_subtitles_args_str = ",".join(ffmpeg_subtitles_args)

        output_video_path = (
            f"{self.video_name}_sub_{'_'.join(self.subtitles.languages)}.mp4"
        )

        result = subprocess.run(
            [
                "ffmpeg",
                "-i",
                self.video_path,
                "-vf",
                ffmpeg_subtitles_args_str,
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

    def translate_subtitles(self):
        prompt = f"""
        Translate the following subtitles to {
            self.subtitles.languages
        }. Original language is {self.subtitles.original_language}.
        The subtitles are:
        {self.subtitles.subtitles[self.subtitles.original_language]}

        Double check original subtitle, fix it if there was an typo, missleading pronounce, or anything with your knowledge. But make sure not out of context.

        Additional Context about the video: {self.context}

        Return the subtitles in the following json array format. Each language should have its own array.
        Example:
        """

        prompt += """\n
        ```json
        "en": [
            {
            "start": 0.0,
                "end": 1.0,
                "text": "Hello, world!"
            },
            {
            "start": 1.5,
                "end": 2.5,
                "text": "Hello, world! 2"
            }
        ],
        "id": [
            {
            "start": 0.0,
                "end": 1.0,
                "text": "Halo, dunia!"
            },
            {
            "start": 1.5,
                "end": 2.5,
                "text": "Halo, dunia! 2"
            }
        ]
        ```
        """
        response = self.openai_client.send_message(
            message=prompt, response_with_json=True
        )
        for language, subtitles in json.loads(response).items():
            self.subtitles.subtitles[language] = subtitles

    def generate_subtitles(
        self, translation_languages: list[str] | None = None
    ) -> Subtitles:
        self.subtitles: Subtitles = Subtitles()

        self.convert_video_to_audio()
        audio = whisper.load_audio(self.audio_path)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(
            audio, n_mels=self.whisper_model.dims.n_mels
        ).to(self.whisper_model.device)
        _, probs = self.whisper_model.detect_language(mel)
        self.subtitles.original_language = max(probs, key=probs.get)
        if translation_languages:
            self.subtitles.languages = translation_languages
        else:
            self.subtitles.languages = [self.subtitles.original_language]

        result = self.whisper_model.transcribe(self.audio_path)
        self.subtitles.subtitles[self.subtitles.original_language] = [
            {
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"],
            }
            for segment in result["segments"]
        ]

        self.translate_subtitles()

        self.subtitle_paths = self.subtitles.save_to_srt(self.video_name)
        self.insert_subtitles_to_video()

        os.remove(self.audio_path)
        for subtitle_path in self.subtitle_paths:
            os.remove(subtitle_path)

        return self.subtitles


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
