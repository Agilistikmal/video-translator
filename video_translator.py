import argparse

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

    def save_subtitles(self, subtitles: Subtitles, output_path: str) -> None:
        if not output_path.endswith(".srt"):
            raise ValueError("Output path must end with .srt")

        with open(output_path, "w") as f:
            for index, subtitle in enumerate(subtitles["subtitles"]):
                f.write(f"{index + 1}\n")
                f.write(f"{subtitle['start']} --> {subtitle['end']}\n")
                f.write(f"{subtitle['text']}\n")
                f.write("\n")


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
