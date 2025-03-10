"""
Song schema for domain model
"""

from dataclasses import dataclass
from typing import Any

from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.song.base_song_schema import BaseSongDAO, BaseSongDTO


@dataclass
class SongDAO(BaseSongDAO):
    """Represents song data in the persistence layer"""


@dataclass
class SongDTO(BaseSongDTO):
    """Represents song metadata and payload in the endpoints"""

    """The streaming url of the song"""
    url: str


def get_song_dao_from_document(document: dict[str, Any]) -> SongDAO:
    """Get SongDAO from document

    Args:
        document (dict): song document

    Returns:
        SongDAO: SongDAO Object

    """
    return SongDAO(
        name=document["name"],
        photo=document["photo"],
        artist=document["artist"],
        seconds_duration=document["duration"],
        genre=Genre(document["genre"]),
        streams=document["streams"],
    )


def get_song_dto_from_dao(song_dao: SongDAO, url: str) -> SongDTO:
    """Get SongDTO from SongDAO

    Args:
        song_dao (SongDAO): SongDAO object
        url (str): song streaming url

    Returns:
        SongDTO: SongDTO object

    """
    return SongDTO(
        name=song_dao.name,
        photo=song_dao.photo,
        artist=song_dao.artist,
        seconds_duration=song_dao.seconds_duration,
        genre=song_dao.genre,
        streams=song_dao.streams,
        url=url,
    )


class SongGetUrlStreamingError(SpotifyElectronError):
    """Get Song url for streaming error"""

    ERROR = "Unexpected error getting streaming url of Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongCreateSongStreamingError(SpotifyElectronError):
    """Song creation"""

    ERROR = "Unexpected error creating Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongDeleteSongStreamingError(SpotifyElectronError):
    """Song deletion"""

    ERROR = "Unexpected error deleting Song"

    def __init__(self):
        super().__init__(self.ERROR)
