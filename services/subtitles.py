from typing import TypedDict


class Subtitle(TypedDict):
    start: float
    end: float
    text: str


class Subtitles:
    def __init__(self):
        self.original_language: str = None
        self.languages: list[str] = None
        self.subtitles: dict[str, list[Subtitle]] = {}

    def seconds_to_srt_time(self, seconds: float) -> str:
        total_seconds = int(seconds)
        milliseconds = int((seconds - total_seconds) * 1000)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def save_to_srt(self, prefix: str) -> list[str]:
        paths = []
        for language, subtitles in self.subtitles.items():
            path = f"{prefix}_sub_{language}.srt"
            with open(path, "w") as f:
                for index, subtitle in enumerate(subtitles):
                    f.write(f"{index + 1}\n")
                    f.write(
                        f"{self.seconds_to_srt_time(subtitle['start'])} --> {self.seconds_to_srt_time(subtitle['end'])}\n"
                    )
                    f.write(f"{subtitle['text']}\n")
                    f.write("\n")
            paths.append(path)
        return paths
