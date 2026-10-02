"""Mio application entry point."""

import logging
import sys

from mio.app import MioApplication


def main() -> int:
    """Entry point for the Mio application.

    Creates the MioApplication, starts the Qt event loop,
    and returns the process exit code.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    app = MioApplication(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
