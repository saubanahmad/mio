"""Tests for PetWindow mouse-based dragging."""

from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from mio.presentation.pet.pet_window import PetWindow


def _make_mouse_event(
    event_type: QMouseEvent.Type,
    local_pos: QPoint,
    global_pos: QPoint,
    button: Qt.MouseButton = Qt.MouseButton.LeftButton,
    buttons: Qt.MouseButton = Qt.MouseButton.LeftButton,
) -> QMouseEvent:
    """Create a QMouseEvent with the given parameters.

    This helper avoids depending on exact desktop coordinates by
    explicitly specifying both local and global positions.
    """
    return QMouseEvent(
        event_type,
        QPointF(local_pos),
        QPointF(global_pos),
        button,
        buttons,
        Qt.KeyboardModifier.NoModifier,
    )


class TestDragInitialState:
    """Dragging should be inactive by default."""

    def test_not_dragging_initially(self, qapp):
        """A freshly created PetWindow should not be in a dragging state."""
        window = PetWindow()
        assert window.is_dragging is False


class TestDragStart:
    """Left mouse press should start dragging."""

    def test_left_press_starts_dragging(self, qapp):
        """Pressing the left mouse button should activate dragging."""
        window = PetWindow()
        window.move(100, 100)

        local_pos = QPoint(50, 50)
        global_pos = QPoint(150, 150)

        event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonPress,
            local_pos,
            global_pos,
        )
        window.mousePressEvent(event)

        assert window.is_dragging is True

    def test_right_press_does_not_start_dragging(self, qapp):
        """Pressing the right mouse button should NOT activate dragging."""
        window = PetWindow()

        local_pos = QPoint(50, 50)
        global_pos = QPoint(150, 150)

        event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonPress,
            local_pos,
            global_pos,
            button=Qt.MouseButton.RightButton,
            buttons=Qt.MouseButton.RightButton,
        )
        window.mousePressEvent(event)

        assert window.is_dragging is False


class TestDragMovement:
    """Mouse movement while dragging should move the window."""

    def test_move_while_dragging_repositions_window(self, qapp):
        """Moving the mouse while dragging should move the window."""
        window = PetWindow()
        window.move(100, 100)

        # Press at local (50, 50) which is global (150, 150).
        press_local = QPoint(50, 50)
        press_global = QPoint(150, 150)
        press_event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonPress,
            press_local,
            press_global,
        )
        window.mousePressEvent(press_event)

        # Move the mouse to global (200, 220).
        # The offset was (150 - 100, 150 - 100) = (50, 50).
        # So the new window pos should be (200 - 50, 220 - 50) = (150, 170).
        move_global = QPoint(200, 220)
        move_local = QPoint(100, 120)  # relative to new expected window pos
        move_event = _make_mouse_event(
            QMouseEvent.Type.MouseMove,
            move_local,
            move_global,
            button=Qt.MouseButton.NoButton,
            buttons=Qt.MouseButton.LeftButton,
        )
        window.mouseMoveEvent(move_event)

        assert window.pos() == QPoint(150, 170)

    def test_move_without_dragging_does_not_move_window(self, qapp):
        """Moving the mouse without a prior press should not move the window."""
        window = PetWindow()
        window.move(100, 100)
        original_pos = window.pos()

        move_event = _make_mouse_event(
            QMouseEvent.Type.MouseMove,
            QPoint(60, 60),
            QPoint(160, 160),
            button=Qt.MouseButton.NoButton,
            buttons=Qt.MouseButton.LeftButton,
        )
        window.mouseMoveEvent(move_event)

        assert window.pos() == original_pos


class TestDragEnd:
    """Releasing the mouse button should end dragging."""

    def test_left_release_ends_dragging(self, qapp):
        """Releasing the left mouse button should deactivate dragging."""
        window = PetWindow()
        window.move(100, 100)

        # Start dragging.
        press_event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonPress,
            QPoint(50, 50),
            QPoint(150, 150),
        )
        window.mousePressEvent(press_event)
        assert window.is_dragging is True

        # Release.
        release_event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonRelease,
            QPoint(50, 50),
            QPoint(150, 150),
            button=Qt.MouseButton.LeftButton,
            buttons=Qt.MouseButton.NoButton,
        )
        window.mouseReleaseEvent(release_event)

        assert window.is_dragging is False

    def test_move_after_release_does_not_move_window(self, qapp):
        """Moving after release should not reposition the window."""
        window = PetWindow()
        window.move(100, 100)

        # Start dragging.
        press_event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonPress,
            QPoint(50, 50),
            QPoint(150, 150),
        )
        window.mousePressEvent(press_event)

        # Release.
        release_event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonRelease,
            QPoint(50, 50),
            QPoint(150, 150),
            button=Qt.MouseButton.LeftButton,
            buttons=Qt.MouseButton.NoButton,
        )
        window.mouseReleaseEvent(release_event)

        # Record position after release.
        pos_after_release = window.pos()

        # Move mouse — should have no effect.
        move_event = _make_mouse_event(
            QMouseEvent.Type.MouseMove,
            QPoint(80, 80),
            QPoint(300, 300),
            button=Qt.MouseButton.NoButton,
            buttons=Qt.MouseButton.NoButton,
        )
        window.mouseMoveEvent(move_event)

        assert window.pos() == pos_after_release


class TestDragOffsetPreservation:
    """The cursor-to-window offset must be preserved during dragging."""

    def test_offset_is_preserved(self, qapp):
        """The cursor offset from the window origin should stay constant."""
        window = PetWindow()
        window.move(200, 300)

        # Press at local (30, 40), global (230, 340).
        # Offset = global - window pos = (230-200, 340-300) = (30, 40).
        press_event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonPress,
            QPoint(30, 40),
            QPoint(230, 340),
        )
        window.mousePressEvent(press_event)

        # Move to global (400, 500).
        # Expected window pos = (400-30, 500-40) = (370, 460).
        move_event = _make_mouse_event(
            QMouseEvent.Type.MouseMove,
            QPoint(30, 40),
            QPoint(400, 500),
            button=Qt.MouseButton.NoButton,
            buttons=Qt.MouseButton.LeftButton,
        )
        window.mouseMoveEvent(move_event)

        expected = QPoint(370, 460)
        assert window.pos() == expected

    def test_offset_varies_by_click_position(self, qapp):
        """Clicking at different local positions should produce different offsets."""
        window = PetWindow()
        window.move(100, 100)

        # Click at local (10, 10), global (110, 110).
        press_event_1 = _make_mouse_event(
            QMouseEvent.Type.MouseButtonPress,
            QPoint(10, 10),
            QPoint(110, 110),
        )
        window.mousePressEvent(press_event_1)

        move_event_1 = _make_mouse_event(
            QMouseEvent.Type.MouseMove,
            QPoint(10, 10),
            QPoint(200, 200),
            button=Qt.MouseButton.NoButton,
            buttons=Qt.MouseButton.LeftButton,
        )
        window.mouseMoveEvent(move_event_1)
        pos_1 = window.pos()  # Should be (200-10, 200-10) = (190, 190)

        # Release and reset.
        release_event = _make_mouse_event(
            QMouseEvent.Type.MouseButtonRelease,
            QPoint(10, 10),
            QPoint(200, 200),
            button=Qt.MouseButton.LeftButton,
            buttons=Qt.MouseButton.NoButton,
        )
        window.mouseReleaseEvent(release_event)
        window.move(100, 100)

        # Click at local (90, 90), global (190, 190).
        press_event_2 = _make_mouse_event(
            QMouseEvent.Type.MouseButtonPress,
            QPoint(90, 90),
            QPoint(190, 190),
        )
        window.mousePressEvent(press_event_2)

        move_event_2 = _make_mouse_event(
            QMouseEvent.Type.MouseMove,
            QPoint(90, 90),
            QPoint(200, 200),
            button=Qt.MouseButton.NoButton,
            buttons=Qt.MouseButton.LeftButton,
        )
        window.mouseMoveEvent(move_event_2)
        pos_2 = window.pos()  # Should be (200-90, 200-90) = (110, 110)

        assert pos_1 == QPoint(190, 190)
        assert pos_2 == QPoint(110, 110)
        assert pos_1 != pos_2
