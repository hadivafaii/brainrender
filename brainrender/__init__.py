import os
import sys
from os.path import join as pjoin
from loguru import logger
from pathlib import Path
from rich.logging import RichHandler

try:
    from pyinspect import install_traceback
    install_traceback()
except ImportError:
    pass  # fails in notebooks

from . import settings, actors
from .scene import Scene
from .video import VideoMaker, Animation

base_dir = Path(os.path.join(os.path.expanduser("~"), ".brainrender"))
base_dir.mkdir(exist_ok=True)

vedo_path = pjoin(os.environ['HOME'], 'Dropbox/git/vedo/vedo')
sys.path.insert(0, vedo_path)
import vedo
from vedo import Plotter

__version__ = "2.0.3.0rc"

# set logger level


def set_logging(level="INFO", path=None):
    """
    Sets loguru to save all logs to a file i
    brainrender's base directory and to print
    to stdout only logs >= to a given level
    """
    logger.remove()
    # logger.add(sys.stdout, level=level)

    path = path or str(base_dir / "log.log")
    if Path(path).exists():
        Path(path).unlink()
    logger.add(path, level="DEBUG")

    if level == "DEBUG":
        logger.configure(
            handlers=[
                {
                    "sink": RichHandler(level="WARNING", markup=True),
                    "format": "{message}",
                }
            ]
        )


if not settings.DEBUG:
    set_logging()
else:
    set_logging(level="DEBUG")
