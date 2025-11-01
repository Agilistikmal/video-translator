from typing import TypedDict


class Subtitle(TypedDict):
    start: float
    end: float
    text: str


class Subtitles(TypedDict):
    original_language: str
    language: str
    subtitles: list[Subtitle]
