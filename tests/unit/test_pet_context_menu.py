"""Tests for PetWindow context menu interactions."""

from PySide6.QtCore import QPoint
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QApplication

import mio.presentation.pet.pet_window
from mio.presentation.pet.pet_window import PetWindow


class MockAction:
    def __init__(self, text):
        self._text = text

    def text(self):
        return self._text


class MockMenuExitSelected:
    def __init__(self, parent=None):
        self._actions = []

    def addAction(self, text):  # noqa: N802
        action = MockAction(text)
        self._actions.append(action)
        return action

    def exec(self, pos):
        for action in self._actions:
            if action.text() == "Exit":
                return action
        return None


class MockMenuDismissed:
    def __init__(self, parent=None):
        self._actions = []

    def addAction(self, text):  # noqa: N802
        action = MockAction(text)
        self._actions.append(action)
        return action

    def exec(self, pos):
        return None


def test_context_menu_exit_action(qapp, monkeypatch):
    """The context menu should contain an Exit action that quits the application."""
    window = PetWindow()

    quit_called = False

    def mock_quit():
        nonlocal quit_called
        quit_called = True

    monkeypatch.setattr(QApplication.instance(), "quit", mock_quit)
    monkeypatch.setattr(mio.presentation.pet.pet_window, "QMenu", MockMenuExitSelected)

    event = QContextMenuEvent(
        QContextMenuEvent.Reason.Mouse, QPoint(50, 50), QPoint(150, 150)
    )
    window.contextMenuEvent(event)

    assert quit_called is True


def test_context_menu_no_action_does_not_quit(qapp, monkeypatch):
    """If the context menu is dismissed without selecting Exit, the app should not quit."""
    window = PetWindow()

    quit_called = False

    def mock_quit():
        nonlocal quit_called
        quit_called = True

    monkeypatch.setattr(QApplication.instance(), "quit", mock_quit)
    monkeypatch.setattr(mio.presentation.pet.pet_window, "QMenu", MockMenuDismissed)

    event = QContextMenuEvent(
        QContextMenuEvent.Reason.Mouse, QPoint(50, 50), QPoint(150, 150)
    )
    window.contextMenuEvent(event)

    assert quit_called is False
