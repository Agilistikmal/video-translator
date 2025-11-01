import argparse
import json
from typing import Literal

from subtitles import Subtitles


class VideoTranslator:
    def __init__(self, video_path):
        self.video_path = video_path

    def generate_subtitles(
        self, video_path: str, translation_language: str | None = None
    ) -> Subtitles:
        subtitles: Subtitles = {}

        if translation_language:
            subtitles["language"] = translation_language
        else:
            subtitles["language"] = "original"

        return subtitles

    def save_subtitles(
        self,
        subtitles: Subtitles,
        output_path: str,
        format: Literal["srt", "json"] | None,
    ) -> None:
        if format is None:
            if output_path.endswith(".srt"):
                format = "srt"
            elif output_path.endswith(".json"):
                format = "json"
            else:
                raise ValueError("Output path must end with .srt or .json")

        if format is not None:
            output_path = f"{output_path.split('.')[0]}.{format}"

        if format == "srt":
            with open(output_path, "w") as f:
                for index, subtitle in enumerate(subtitles["subtitles"]):
                    f.write(f"{index + 1}\n")
                    f.write(f"{subtitle['start']} --> {subtitle['end']}\n")
                    f.write(f"{subtitle['text']}\n")
                    f.write("\n")

        elif format == "json":
            with open(output_path, "w") as f:
                json.dump(subtitles, f, indent=4)


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
