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

    try:
        app = MioApplication(sys.argv)
        return app.run()
    except Exception as e:
        logging.getLogger(__name__).critical("Fatal application error: %s", e, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
