"""Tests for the Mio application lifecycle."""

import pytest
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from mio.app import MioApplication


class TestMioApplicationInit:
    """Tests for MioApplication initialization."""

    def test_creates_qt_application(self, qapp):
        """MioApplication should hold a QApplication instance."""
        mio_app = MioApplication(args=[])
        assert isinstance(mio_app.qt_app, QApplication)

    def test_sets_application_name(self, qapp):
        """MioApplication should set the application name to 'Mio'."""
        mio_app = MioApplication(args=[])
        assert mio_app.qt_app.applicationName() == "Mio"

    def test_sets_application_version(self, qapp):
        """MioApplication should set the application version."""
        mio_app = MioApplication(args=[])
        assert mio_app.qt_app.applicationVersion() == "0.1.0"

    def test_reuses_existing_qapplication(self, qapp):
        """MioApplication should reuse an existing QApplication."""
        mio_app = MioApplication(args=[])
        assert mio_app.qt_app is qapp

    def test_fails_gracefully_if_pet_window_fails(self, qapp, monkeypatch):
        """MioApplication should raise RuntimeError if PetWindow fails to initialize."""
        import mio.app

        def mock_pet_window_init(*args, **kwargs):
            raise ValueError("Simulated window failure")

        monkeypatch.setattr(mio.app, "PetWindow", mock_pet_window_init)

        with pytest.raises(RuntimeError, match="Application initialization failed"):
            MioApplication(args=[])


class TestMioApplicationLifecycle:
    """Tests for MioApplication start/stop lifecycle."""

    def test_quit_causes_clean_exit(self, qapp):
        """Calling quit() should cause the event loop to stop with code 0."""
        mio_app = MioApplication(args=[])

        # Schedule quit shortly after the event loop starts.
        QTimer.singleShot(50, mio_app.quit)

        exit_code = mio_app.run()
        assert exit_code == 0

    def test_run_returns_integer(self, qapp):
        """run() should return an integer exit code."""
        mio_app = MioApplication(args=[])

        QTimer.singleShot(50, mio_app.quit)

        exit_code = mio_app.run()
        assert isinstance(exit_code, int)

    def test_run_returns_1_if_already_running(self, qapp):
        """run() should return 1 if called while already running."""
        mio_app = MioApplication(args=[])
        mio_app._running = True

        exit_code = mio_app.run()
        assert exit_code == 1

    def test_run_catches_exceptions_and_cleans_up(self, qapp, monkeypatch):
        """run() should catch exceptions, return 1, and ensure cleanup is called."""
        mio_app = MioApplication(args=[])

        def mock_exec():
            raise RuntimeError("Simulated event loop crash")

        monkeypatch.setattr(mio_app.qt_app, "exec", mock_exec)

        exit_code = mio_app.run()
        assert exit_code == 1
        assert not mio_app._running
        assert mio_app._shutting_down

    def test_cleanup_is_idempotent(self, qapp):
        """cleanup() should safely execute multiple times without error."""
        mio_app = MioApplication(args=[])

        mio_app.cleanup()
        assert mio_app._shutting_down

        # Second call should return early, not crashing
        mio_app.cleanup()
        assert mio_app._shutting_down
