"""Pytest configuration for Mio tests.

Configures pytest-qt to use PySide6 as the Qt binding.
"""

import pytest


@pytest.fixture()
def mio_app():
    """Create a MioApplication instance for testing.

    pytest-qt's qapp fixture manages the underlying QApplication singleton,
    so MioApplication is constructed with qapp_args=[] to reuse it.
    """
    from mio.app import MioApplication

    return MioApplication(args=[])
