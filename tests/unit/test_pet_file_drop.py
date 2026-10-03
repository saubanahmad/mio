"""Tests for PetWindow drag and drop interactions."""

from PySide6.QtCore import QMimeData, QPoint, Qt, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent

from mio.presentation.pet.pet_window import PetWindow


def test_drag_enter_accepts_urls(qapp):
    """dragEnterEvent should accept events with URLs."""
    window = PetWindow()
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile("something")])
    event = QDragEnterEvent(
        QPoint(0, 0),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    window.dragEnterEvent(event)
    assert event.isAccepted()


def test_drag_enter_ignores_non_urls(qapp):
    """dragEnterEvent should ignore events without URLs."""
    window = PetWindow()
    mime = QMimeData()
    mime.setText("just text")
    event = QDragEnterEvent(
        QPoint(0, 0),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    event.ignore()
    window.dragEnterEvent(event)
    assert not event.isAccepted()


def test_drop_event_valid_file_and_dir(qapp, tmp_path):
    """dropEvent should correctly validate files and directories."""
    window = PetWindow()

    test_file = tmp_path / "test.txt"
    test_file.touch()

    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    mime = QMimeData()
    mime.setUrls([
        QUrl.fromLocalFile(str(test_file)),
        QUrl.fromLocalFile(str(test_dir)),
    ])

    event = QDropEvent(
        QPoint(0, 0),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    emitted = []
    window.files_dropped.connect(emitted.append)

    window.dropEvent(event)

    assert event.isAccepted()
    assert len(emitted) == 1

    drop_event = emitted[0]
    assert len(drop_event.paths) == 2
    assert len(drop_event.valid_paths) == 2
    assert len(drop_event.invalid_paths) == 0
    assert test_file in drop_event.valid_paths
    assert test_dir in drop_event.valid_paths


def test_drop_event_invalid_paths(qapp, tmp_path):
    """dropEvent should correctly categorize invalid/missing paths."""
    window = PetWindow()

    missing = tmp_path / "missing.txt"

    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(str(missing))])

    event = QDropEvent(
        QPoint(0, 0),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    emitted = []
    window.files_dropped.connect(emitted.append)

    window.dropEvent(event)

    assert len(emitted) == 1

    drop_event = emitted[0]
    assert len(drop_event.paths) == 1
    assert len(drop_event.valid_paths) == 0
    assert len(drop_event.invalid_paths) == 1
    assert missing in drop_event.invalid_paths


def test_drop_event_empty_urls(qapp):
    """dropEvent should return early if no URLs are present."""
    window = PetWindow()

    mime = QMimeData()
    event = QDropEvent(
        QPoint(0, 0),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )

    emitted = []
    window.files_dropped.connect(emitted.append)

    window.dropEvent(event)

    assert len(emitted) == 0
