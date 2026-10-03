"""Mio animation controller.

Maps semantic pet states to animation assets and manages playback.

This module belongs to the Presentation layer. It connects the
application-level PetState to visual animation resources without
containing business logic.

The controller follows the architecture:
    PetState → Animation Controller → Visual Animation

Animation assets are located by convention: each PetState member
corresponds to a GIF file named ``{state_name_lowercase}.gif``
in the configured assets directory.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtGui import QMovie

from mio.pet_state import PetState

logger = logging.getLogger(__name__)


class AnimationController:
    """Maps PetState values to animation assets.

    Responsibilities:
        - Discover animation assets for each PetState by convention.
        - Create QMovie instances for playback.
        - Switch the active animation when the pet state changes.
        - Ensure the previous animation is stopped before starting a new one.

    The controller does NOT:
        - Contain business logic or state-transition logic.
        - Own or manage the widget that displays the animation.
        - Determine when state changes should occur.

    Asset convention:
        Each ``PetState`` member maps to a GIF file named
        ``{state.name.lower()}.gif`` in the assets directory.
        For example, ``PetState.IDLE`` → ``idle.gif``.
    """

    def __init__(self, assets_dir: Path) -> None:
        if not assets_dir.is_dir():
            raise FileNotFoundError(
                f"Animation assets directory does not exist: {assets_dir}"
            )

        self._assets_dir = assets_dir
        self._asset_paths = self._discover_assets()
        self._current_movie: QMovie | None = None
        self._current_state: PetState | None = None

        logger.info(
            "AnimationController created with %d asset(s) from %s.",
            len(self._asset_paths),
            assets_dir,
        )

    @property
    def current_state(self) -> PetState | None:
        """The PetState currently being animated, or None if not started."""
        return self._current_state

    @property
    def current_movie(self) -> QMovie | None:
        """The active QMovie instance, or None if no animation is playing."""
        return self._current_movie

    @property
    def assets_dir(self) -> Path:
        """The directory where animation assets are located."""
        return self._assets_dir

    def _discover_assets(self) -> dict[PetState, Path]:
        """Discover which PetState values have corresponding asset files.

        Returns:
            A mapping from PetState to the resolved asset file path.
        """
        mapping: dict[PetState, Path] = {}
        for state in PetState:
            path = self._assets_dir / f"{state.name.lower()}.gif"
            if path.is_file():
                mapping[state] = path
                logger.debug("Found asset for %s: %s", state.name, path)
            else:
                logger.warning("No asset found for %s (expected: %s)", state.name, path)
        return mapping

    def has_asset(self, state: PetState) -> bool:
        """Check whether an animation asset exists for the given state."""
        return state in self._asset_paths

    def get_asset_path(self, state: PetState) -> Path | None:
        """Get the asset file path for a state, or None if not found."""
        return self._asset_paths.get(state)

    def set_state(self, state: PetState) -> QMovie | None:
        """Switch to the animation for the given state.

        Stops the current animation (if any), creates a new QMovie for
        the requested state, and starts it.

        Args:
            state: The PetState to animate.

        Returns:
            The new QMovie instance, or None if no asset exists for the state.

        Raises:
            ValueError: If an asset file exists but produces an invalid QMovie.
        """
        if state == self._current_state and self._current_movie is not None:
            return self._current_movie

        # Stop the previous animation.
        if self._current_movie is not None:
            self._current_movie.stop()
            self._current_movie = None

        self._current_state = state

        asset_path = self._asset_paths.get(state)
        if asset_path is None:
            logger.warning("No animation asset for state %s.", state.name)
            return None

        movie = QMovie(str(asset_path))
        if not movie.isValid():
            raise ValueError(
                f"Animation asset is invalid: {asset_path}"
            )

        movie.start()
        self._current_movie = movie

        logger.debug("Animation switched to %s (%s).", state.name, asset_path.name)
        return movie

    def stop(self) -> None:
        """Stop the current animation and release the QMovie."""
        if self._current_movie is not None:
            self._current_movie.stop()
            self._current_movie = None
        self._current_state = None
