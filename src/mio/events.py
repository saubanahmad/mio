"""Application events.

This module defines structured events that the application can produce
or coordinate. These act as the boundary between the presentation layer
and the application coordination layer.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileDropEvent:
    """An event representing filesystem paths dropped onto the application.

    Attributes:
        paths: All local filesystem paths extracted from the drop.
        valid_paths: Paths that exist and are accessible.
        invalid_paths: Paths that do not exist or are inaccessible.
    """
    paths: list[Path]
    valid_paths: list[Path]
    invalid_paths: list[Path]
