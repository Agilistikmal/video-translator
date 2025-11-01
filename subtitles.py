from typing import TypedDict


class Subtitle(TypedDict):
    start: float
    end: float
    text: str


class Subtitles(TypedDict):
    language: str
    subtitles: list[Subtitle]
