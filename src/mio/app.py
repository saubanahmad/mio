"""Mio application lifecycle.

This module provides the core application coordination for Mio.
It owns the QApplication instance and manages startup/shutdown.
"""

import contextlib
import logging
import sys

from PySide6.QtWidgets import QApplication

from mio.events import FileDropEvent
from mio.presentation.pet.pet_window import PetWindow

logger = logging.getLogger(__name__)


class MioApplication:
    """Core Mio application lifecycle manager.

    Responsibilities:
        - Create and own the QApplication instance (or reuse an existing one).
        - Create and own the pet window.
        - Manage startup and shutdown.
        - Provide the main event loop entry point.

    This class belongs to the Application Coordination layer.
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

        self._running = False
        self._shutting_down = False

        self._qt_app.setApplicationName("Mio")
        self._qt_app.setApplicationVersion("0.1.0")

        try:
            self._pet_window = PetWindow()
            self._pet_window.files_dropped.connect(self._on_files_dropped)
        except Exception as e:
            logger.error("Failed to initialize PetWindow: %s", e, exc_info=True)
            raise RuntimeError("Application initialization failed.") from e

        logger.info("Mio application initialized.")

    def _on_files_dropped(self, event: FileDropEvent) -> None:
        """Handle a file drop event from the presentation layer."""
        logger.info(
            "File drop event received: %d valid, %d invalid",
            len(event.valid_paths),
            len(event.invalid_paths),
        )

    @property
    def qt_app(self) -> QApplication:
        """Access the underlying QApplication instance."""
        return self._qt_app

    @property
    def pet_window(self) -> PetWindow:
        """Access the pet window instance."""
        return self._pet_window

    def run(self) -> int:
        """Start the Qt event loop and return the exit code.

        Shows the pet window, then enters the event loop.

        Returns:
            The process exit code from QApplication.exec() or 1 on error.
        """
        if self._running:
            logger.warning("Mio application is already running.")
            return 1

        self._running = True
        logger.info("Mio application starting.")

        try:
            self._pet_window.show()
            exit_code = self._qt_app.exec()
            logger.info("Mio application exited with code %d.", exit_code)
            return exit_code
        except Exception as e:
            logger.error(
                "Application encountered a fatal error during execution: %s", e, exc_info=True
            )
            return 1
        finally:
            self.cleanup()
            self._running = False

    def cleanup(self) -> None:
        """Clean up application resources.

        Safely disconnects signals and closes the presentation layer.
        """
        if self._shutting_down:
            return

        self._shutting_down = True
        logger.info("Cleaning up application resources.")

        if hasattr(self, "_pet_window") and self._pet_window is not None:
            with contextlib.suppress(RuntimeError, TypeError):
                self._pet_window.files_dropped.disconnect(self._on_files_dropped)
            self._pet_window.close()

    def quit(self) -> None:
        """Request the application to quit."""
        logger.info("Application quit requested.")
        self._qt_app.quit()
