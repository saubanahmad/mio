"""Mio pet window.

Provides the frameless, transparent desktop companion window.
This is the primary visual container for the Mio pet.

This module belongs to the Presentation layer and must not contain
business logic, utility operations, or application-wide coordination.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QContextMenuEvent, QDragEnterEvent, QDropEvent, QMouseEvent, QPainter
from PySide6.QtWidgets import QApplication, QMenu, QToolTip, QWidget

from mio.events import FileDropEvent
from mio.pet_state import PetState
from mio.presentation.pet.animation_controller import AnimationController

logger = logging.getLogger(__name__)

# Window dimensions for the pet container.
_PET_WINDOW_WIDTH = 200
_PET_WINDOW_HEIGHT = 200

# Default assets directory, resolved relative to the project root.
# This assumes the standard development layout where pet_window.py is at
# src/mio/presentation/pet/pet_window.py and assets are at assets/pet/.
_DEFAULT_ASSETS_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent.parent / "assets" / "pet"
)


class PetWindow(QWidget):
    """Frameless, transparent window that displays the Mio pet.

    Responsibilities:
        - Frameless, transparent window configuration.
        - Rendering the pet animation for the current state.
        - Providing a correctly sized and positioned desktop container.
        - Mouse-based dragging to reposition the pet on the desktop.
        - Tracking the current pet state.

    This window does NOT handle:
        - Context menus (later increments).
        - Any business logic, utility operations, or AI.
    """

    files_dropped = Signal(FileDropEvent)

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        assets_dir: Path | None = None,
    ) -> None:
        super().__init__(parent)

        self._pet_state = PetState.IDLE
        self._dragging = False
        self._drag_offset = QPoint()

        self._configure_window()
        self._set_initial_geometry()

        # Animation.
        resolved_assets_dir = assets_dir if assets_dir is not None else _DEFAULT_ASSETS_DIR
        self._animation_controller = AnimationController(resolved_assets_dir)
        self._animation_controller.set_state(PetState.IDLE)

        # Connect QMovie frame updates to widget repaint.
        movie = self._animation_controller.current_movie
        if movie is not None:
            movie.frameChanged.connect(self.update)

        logger.info("PetWindow created.")

    @property
    def animation_controller(self) -> AnimationController:
        """Access the animation controller."""
        return self._animation_controller

    # --- Pet State ----------------------------------------------------------

    @property
    def pet_state(self) -> PetState:
        """The current semantic state of the pet."""
        return self._pet_state

    @pet_state.setter
    def pet_state(self, state: PetState) -> None:
        """Set the pet state and switch the animation.

        Args:
            state: A valid PetState enum member.

        Raises:
            TypeError: If the value is not a PetState member.
        """
        if not isinstance(state, PetState):
            raise TypeError(
                f"pet_state must be a PetState member, got {type(state).__name__}"
            )
        if state == self._pet_state:
            return

        self._pet_state = state
        self._switch_animation(state)

    def _switch_animation(self, state: PetState) -> None:
        """Switch the active animation to match the given state."""
        # Disconnect the old movie's signal if present.
        old_movie = self._animation_controller.current_movie
        if old_movie is not None:
            old_movie.frameChanged.disconnect(self.update)

        movie = self._animation_controller.set_state(state)

        # Connect the new movie's signal.
        if movie is not None:
            movie.frameChanged.connect(self.update)

        self.update()

    # --- Dragging -----------------------------------------------------------

    @property
    def is_dragging(self) -> bool:
        """Whether the pet is currently being dragged."""
        return self._dragging

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Begin dragging on left mouse button press."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self.pet_state = PetState.DRAGGING
            self._drag_offset = event.globalPosition().toPoint() - self.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Move the window to follow the cursor while dragging."""
        if self._dragging:
            self.move(event.globalPosition().toPoint() - self._drag_offset)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """End dragging on left mouse button release."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            self.pet_state = PetState.IDLE
        super().mouseReleaseEvent(event)

    # --- Drag and Drop ------------------------------------------------------

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:  # noqa: N802
        """Accept drag events containing URLs/files."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:  # noqa: N802
        """Handle file drops."""
        urls = event.mimeData().urls()
        if not urls:
            return

        all_paths = []
        valid_paths = []
        invalid_paths = []

        for url in urls:
            if url.isLocalFile():
                path_str = url.toLocalFile()
                path = Path(path_str)
                all_paths.append(path)
                try:
                    if path.exists():
                        valid_paths.append(path)
                    else:
                        invalid_paths.append(path)
                except OSError:
                    invalid_paths.append(path)

        drop_event = FileDropEvent(
            paths=all_paths,
            valid_paths=valid_paths,
            invalid_paths=invalid_paths,
        )
        self.files_dropped.emit(drop_event)

        # Basic visual feedback
        msg = f"Received {len(valid_paths)} item(s)"
        if invalid_paths:
            msg += f"\nSkipped {len(invalid_paths)} invalid item(s)"
        QToolTip.showText(self.mapToGlobal(event.position().toPoint()), msg, self)

        event.acceptProposedAction()

    # --- Context Menu -------------------------------------------------------

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:  # noqa: N802
        """Show the context menu."""
        menu = QMenu(self)
        exit_action = menu.addAction("Exit")

        action = menu.exec(event.globalPos())
        if action == exit_action:
            QApplication.instance().quit()

    # --- Window Configuration -----------------------------------------------

    def _configure_window(self) -> None:
        """Apply Qt flags and attributes for a desktop companion window."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowTitle("Mio")
        self.setAcceptDrops(True)

    def _set_initial_geometry(self) -> None:
        """Set initial window size and position.

        Places the pet near the bottom-right of the primary screen,
        offset inward so it is comfortably visible.
        """
        self.resize(_PET_WINDOW_WIDTH, _PET_WINDOW_HEIGHT)

        screen = self.screen()
        if screen is not None:
            available = screen.availableGeometry()
            x = available.right() - _PET_WINDOW_WIDTH - 80
            y = available.bottom() - _PET_WINDOW_HEIGHT - 80
            self.move(x, y)

    # --- Painting -----------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        """Render the current animation frame.

        Draws the current QMovie frame centered in the widget.
        If no animation is available, the widget remains transparent.
        """
        movie = self._animation_controller.current_movie
        if movie is None:
            return

        pixmap = movie.currentPixmap()
        if pixmap.isNull():
            return

        painter = QPainter(self)
        # Center the animation frame in the window.
        x = (self.width() - pixmap.width()) // 2
        y = (self.height() - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)
        painter.end()
