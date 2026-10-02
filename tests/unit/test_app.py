"""Tests for the Mio application lifecycle."""

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
