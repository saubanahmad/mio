"""Tests for the Mio animation controller."""

from pathlib import Path

import pytest
from PySide6.QtGui import QMovie

from mio.pet_state import PetState
from mio.presentation.pet.animation_controller import AnimationController


class TestAnimationControllerInitialization:
    """Tests for AnimationController startup."""

    def test_missing_directory_raises_error(self, tmp_path):
        """Passing a non-existent directory raises FileNotFoundError."""
        bad_dir = tmp_path / "does_not_exist"
        with pytest.raises(FileNotFoundError, match="Animation assets directory does not exist"):
            AnimationController(bad_dir)

    def test_discovers_existing_assets(self, tmp_path, qapp):
        """The controller should find assets matching the {state}.gif convention."""
        (tmp_path / "idle.gif").touch()
        (tmp_path / "dragging.gif").touch()

        controller = AnimationController(tmp_path)

        assert controller.has_asset(PetState.IDLE)
        assert controller.has_asset(PetState.DRAGGING)
        assert controller.get_asset_path(PetState.IDLE) == tmp_path / "idle.gif"

    def test_handles_missing_assets_gracefully(self, tmp_path, qapp):
        """If an asset is missing, it should just not be discovered."""
        (tmp_path / "idle.gif").touch()
        # dragging.gif is intentionally missing

        controller = AnimationController(tmp_path)

        assert controller.has_asset(PetState.IDLE)
        assert not controller.has_asset(PetState.DRAGGING)
        assert controller.get_asset_path(PetState.DRAGGING) is None


class TestAnimationControllerStateSwitching:
    """Tests for switching animation states."""

    def _create_dummy_gif(self, path: Path):
        """Create a valid minimal GIF file."""
        # A tiny transparent 1x1 GIF
        gif_data = (
            b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00"
            b"!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01"
            b"\x00\x00\x02\x02D\x01\x00;"
        )
        path.write_bytes(gif_data)

    def test_set_state_returns_movie_for_valid_asset(self, tmp_path, qapp):
        """set_state should return a playing QMovie for a valid asset."""
        asset_path = tmp_path / "idle.gif"
        self._create_dummy_gif(asset_path)

        controller = AnimationController(tmp_path)
        movie = controller.set_state(PetState.IDLE)

        assert isinstance(movie, QMovie)
        assert movie.isValid()
        assert movie.state() == QMovie.MovieState.Running
        assert controller.current_state == PetState.IDLE
        assert controller.current_movie is movie

    def test_set_state_returns_none_for_missing_asset(self, tmp_path, qapp):
        """set_state should return None if the asset file does not exist."""
        controller = AnimationController(tmp_path)
        movie = controller.set_state(PetState.IDLE)

        assert movie is None
        assert controller.current_state == PetState.IDLE
        assert controller.current_movie is None

    def test_set_state_raises_value_error_for_invalid_asset(self, tmp_path, qapp):
        """set_state should raise ValueError if the file exists but is not a valid animation."""
        asset_path = tmp_path / "idle.gif"
        asset_path.write_text("Not a real gif")

        controller = AnimationController(tmp_path)

        with pytest.raises(ValueError, match="Animation asset is invalid"):
            controller.set_state(PetState.IDLE)

    def test_set_state_stops_previous_movie(self, tmp_path, qapp):
        """Switching states should stop the previously playing movie."""
        idle_path = tmp_path / "idle.gif"
        dragging_path = tmp_path / "dragging.gif"
        self._create_dummy_gif(idle_path)
        self._create_dummy_gif(dragging_path)

        controller = AnimationController(tmp_path)

        idle_movie = controller.set_state(PetState.IDLE)
        assert idle_movie.state() == QMovie.MovieState.Running

        dragging_movie = controller.set_state(PetState.DRAGGING)

        # The previous movie should be stopped
        assert idle_movie.state() == QMovie.MovieState.NotRunning
        assert dragging_movie.state() == QMovie.MovieState.Running
        assert controller.current_movie is dragging_movie
        assert controller.current_state == PetState.DRAGGING

    def test_set_state_same_state_returns_existing_movie(self, tmp_path, qapp):
        """Switching to the same state should return the already playing movie."""
        idle_path = tmp_path / "idle.gif"
        self._create_dummy_gif(idle_path)

        controller = AnimationController(tmp_path)
        movie1 = controller.set_state(PetState.IDLE)
        movie2 = controller.set_state(PetState.IDLE)

        assert movie1 is movie2
        assert movie1.state() == QMovie.MovieState.Running

    def test_stop_clears_current_movie(self, tmp_path, qapp):
        """Calling stop() should stop playback and clear the current state."""
        idle_path = tmp_path / "idle.gif"
        self._create_dummy_gif(idle_path)

        controller = AnimationController(tmp_path)
        movie = controller.set_state(PetState.IDLE)

        controller.stop()

        assert movie.state() == QMovie.MovieState.NotRunning
        assert controller.current_movie is None
        assert controller.current_state is None
