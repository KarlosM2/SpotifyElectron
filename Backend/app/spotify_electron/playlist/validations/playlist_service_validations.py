"""
Validations for Playlist service
"""

from app.exceptions.base_exceptions_schema import BadParameterError
from app.spotify_electron.playlist.playlist_repository import check_playlist_exists
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistAlreadyExistsError,
    PlaylistBadNameError,
    PlaylistNotFoundError,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_playlist_name_parameter(name: str) -> None:
    """Raises an exception if playlist name parameter is invalid

    Args:
        name (str): name

    Raises:
        PlaylistBadNameError: if name parameter is invalid

    """
    try:
        validate_parameter(name)
    except BadParameterError:
        raise PlaylistBadNameError from BadParameterError


def validate_playlist_should_exists(name: str) -> None:
    """Raises an exception if playlist doesn't exists

    Args:
        name (str): playlist name

    Raises:
        PlaylistNotFoundError: if playlist doesn't exists

    """
    if not check_playlist_exists(name):
        raise PlaylistNotFoundError


def validate_playlist_should_not_exists(name: str) -> None:
    """Raises an exception if playlist does exists

    Args:
        name (str): playlist name

    Raises:
        PlaylistAlreadyExistsError: if playlist exists

    """
    if check_playlist_exists(name):
        raise PlaylistAlreadyExistsError
