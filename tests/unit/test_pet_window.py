"""Tests for the Mio pet window."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from mio.presentation.pet.pet_window import PetWindow


class TestPetWindowCreation:
    """Tests for PetWindow instantiation and configuration."""

    def test_can_be_instantiated(self, qapp):
        """PetWindow can be created without errors."""
        window = PetWindow()
        assert isinstance(window, QWidget)

    def test_is_frameless(self, qapp):
        """PetWindow must have the FramelessWindowHint flag."""
        window = PetWindow()
        assert window.windowFlags() & Qt.WindowType.FramelessWindowHint

    def test_stays_on_top(self, qapp):
        """PetWindow must have the WindowStaysOnTopHint flag."""
        window = PetWindow()
        assert window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint

    def test_is_tool_window(self, qapp):
        """PetWindow should use the Tool window type to avoid taskbar entry."""
        window = PetWindow()
        assert window.windowFlags() & Qt.WindowType.Tool

    def test_has_translucent_background(self, qapp):
        """PetWindow must have WA_TranslucentBackground enabled."""
        window = PetWindow()
        assert window.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def test_has_valid_size(self, qapp):
        """PetWindow must have a positive, non-zero size."""
        window = PetWindow()
        assert window.width() > 0
        assert window.height() > 0

    def test_window_title_is_mio(self, qapp):
        """PetWindow should have 'Mio' as the window title."""
        window = PetWindow()
        assert window.windowTitle() == "Mio"


class TestPetWindowVisibility:
    """Tests for PetWindow show/hide behavior."""

    def test_can_be_shown(self, qapp):
        """PetWindow can be shown without errors."""
        window = PetWindow()
        window.show()
        assert window.isVisible()
        window.close()

    def test_can_be_closed(self, qapp):
        """PetWindow can be closed cleanly."""
        window = PetWindow()
        window.show()
        window.close()
        assert not window.isVisible()


class TestPetWindowIntegration:
    """Tests for PetWindow integration with MioApplication."""

    def test_mio_app_creates_pet_window(self, qapp):
        """MioApplication should create a PetWindow instance."""
        from mio.app import MioApplication

        mio_app = MioApplication(args=[])
        assert isinstance(mio_app.pet_window, PetWindow)

    def test_pet_window_not_shown_before_run(self, qapp):
        """PetWindow should not be visible until run() is called."""
        from mio.app import MioApplication

        mio_app = MioApplication(args=[])
        assert not mio_app.pet_window.isVisible()


class TestPetWindowAnimationIntegration:
    """Tests for PetWindow integration with AnimationController."""

    def test_window_initializes_with_idle_animation(self, qapp):
        """The PetWindow should start with the IDLE animation."""
        from mio.pet_state import PetState
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()
        assert window.animation_controller.current_state == PetState.IDLE

    def test_state_change_switches_animation(self, qapp):
        """Changing pet_state should switch the animation via the controller."""
        from mio.pet_state import PetState
        from mio.presentation.pet.pet_window import PetWindow

        window = PetWindow()

        window.pet_state = PetState.DRAGGING
        assert window.animation_controller.current_state == PetState.DRAGGING

        window.pet_state = PetState.IDLE
        assert window.animation_controller.current_state == PetState.IDLE

