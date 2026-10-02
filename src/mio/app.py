"""Mio application lifecycle.

This module provides the core application coordination for Mio.
It owns the QApplication instance and manages startup/shutdown.
"""

import logging
import sys

from PySide6.QtWidgets import QApplication

logger = logging.getLogger(__name__)


class MioApplication:
    """Core Mio application lifecycle manager.

    Responsibilities:
        - Create and own the QApplication instance (or reuse an existing one).
        - Manage startup and shutdown.
        - Provide the main event loop entry point.

    This class belongs to the Application Coordination layer.
    It does not own presentation components (pet window, animations, etc.).
    """

    def __init__(self, args: list[str] | None = None) -> None:
        # Reuse an existing QApplication if one already exists (e.g. in tests).
        existing = QApplication.instance()
        if existing is not None:
            self._qt_app = existing
            self._owns_qt_app = False
        else:
            if args is None:
                args = sys.argv
            self._qt_app = QApplication(args)
            self._owns_qt_app = True

        self._qt_app.setApplicationName("Mio")
        self._qt_app.setApplicationVersion("0.1.0")

        logger.info("Mio application initialized.")

    @property
    def qt_app(self) -> QApplication:
        """Access the underlying QApplication instance."""
        return self._qt_app

    def run(self) -> int:
        """Start the Qt event loop and return the exit code.

        Returns:
            The process exit code from QApplication.exec().
        """
        logger.info("Mio application starting.")
        exit_code = self._qt_app.exec()
        logger.info("Mio application exited with code %d.", exit_code)
        return exit_code

    def quit(self) -> None:
        """Request the application to quit."""
        self._qt_app.quit()
