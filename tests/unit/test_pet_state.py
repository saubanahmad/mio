"""Tests for the Mio pet state model."""

import pytest

from mio.pet_state import PetState


class TestPetStateEnum:
    """Tests for the PetState enum definition."""

    def test_has_idle_state(self):
        """PetState must define an IDLE member."""
        assert hasattr(PetState, "IDLE")

    def test_has_dragging_state(self):
        """PetState must define a DRAGGING member."""
        assert hasattr(PetState, "DRAGGING")

    def test_states_are_distinct(self):
        """Each PetState member must have a distinct value."""
        assert PetState.IDLE != PetState.DRAGGING

    def test_idle_is_a_pet_state(self):
        """IDLE should be a PetState instance."""
        assert isinstance(PetState.IDLE, PetState)

    def test_dragging_is_a_pet_state(self):
        """DRAGGING should be a PetState instance."""
        assert isinstance(PetState.DRAGGING, PetState)


class TestPetStateIntegrationWithPetWindow:
    """Tests for PetState integration within PetWindow."""

    def test_initial_state_is_idle(self, qapp):
        """PetWindow should start in the IDLE state."""
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        assert window.pet_state is PetState.IDLE

    def test_state_can_be_read(self, qapp):
        """The pet_state property should return a PetState member."""
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        assert isinstance(window.pet_state, PetState)

    def test_state_can_be_set(self, qapp):
        """The pet state can be changed via the setter."""
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        window.pet_state = PetState.DRAGGING
        assert window.pet_state is PetState.DRAGGING

    def test_state_can_be_set_back_to_idle(self, qapp):
        """The pet state can be changed back to IDLE."""
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        window.pet_state = PetState.DRAGGING
        window.pet_state = PetState.IDLE
        assert window.pet_state is PetState.IDLE

    def test_invalid_state_raises_type_error(self, qapp):
        """Setting a non-PetState value should raise TypeError."""
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        with pytest.raises(TypeError, match="pet_state must be a PetState member"):
            window.pet_state = "IDLE"  # type: ignore[assignment]

    def test_invalid_state_int_raises_type_error(self, qapp):
        """Setting an integer value should raise TypeError."""
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        with pytest.raises(TypeError, match="pet_state must be a PetState member"):
            window.pet_state = 1  # type: ignore[assignment]

    def test_invalid_state_none_raises_type_error(self, qapp):
        """Setting None should raise TypeError."""
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        with pytest.raises(TypeError, match="pet_state must be a PetState member"):
            window.pet_state = None  # type: ignore[assignment]


class TestPetStateDragIntegration:
    """Tests for the state model's integration with dragging."""

    def test_drag_start_sets_dragging_state(self, qapp):
        """Starting a drag should set the state to DRAGGING."""
        from PySide6.QtCore import QPoint, QPointF, Qt
        from PySide6.QtGui import QMouseEvent

        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        window.move(100, 100)
        assert window.pet_state is PetState.IDLE

        event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(QPoint(50, 50)),
            QPointF(QPoint(150, 150)),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        window.mousePressEvent(event)

        assert window.pet_state is PetState.DRAGGING

    def test_drag_end_restores_idle_state(self, qapp):
        """Ending a drag should restore the state to IDLE."""
        from PySide6.QtCore import QPoint, QPointF, Qt
        from PySide6.QtGui import QMouseEvent

        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        window.move(100, 100)

        # Start drag.
        press = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(QPoint(50, 50)),
            QPointF(QPoint(150, 150)),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        window.mousePressEvent(press)
        assert window.pet_state is PetState.DRAGGING

        # End drag.
        release = QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            QPointF(QPoint(50, 50)),
            QPointF(QPoint(150, 150)),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier,
        )
        window.mouseReleaseEvent(release)

        assert window.pet_state is PetState.IDLE

    def test_right_click_does_not_change_state(self, qapp):
        """Right-clicking should not change the pet state."""
        from PySide6.QtCore import QPoint, QPointF, Qt
        from PySide6.QtGui import QMouseEvent

        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        assert window.pet_state is PetState.IDLE

        event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPointF(QPoint(50, 50)),
            QPointF(QPoint(150, 150)),
            Qt.MouseButton.RightButton,
            Qt.MouseButton.RightButton,
            Qt.KeyboardModifier.NoModifier,
        )
        window.mousePressEvent(event)

        assert window.pet_state is PetState.IDLE
