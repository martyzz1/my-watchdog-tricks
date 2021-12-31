import signal
from pathlib import Path

# Third party libraries
from watchdog.utils import echo
from watchdog_tricks.batch import BatchTrick


class TouchFileTrick(BatchTrick):

    """Touches a file whenever other files change. Useful for triggering events from  multiple directories

    The touchfile parameter is a path to a file which will be "touched"

    """

    def __init__(self, touchfile, patterns=None, ignore_patterns=None,
                 ignore_directories=False, stop_signal=signal.SIGINT,
                 kill_after=10, source_directory=None):
        self.touchfile = touchfile
        self.stop_signal = stop_signal
        self.kill_after = kill_after
        self.source_directory = source_directory
        super(TouchFileTrick, self).__init__(
            patterns, ignore_patterns, ignore_directories)

    def touch_file(self):
        print("Touching - {0}".format(self.touchfile))
        Path(self.touchfile).touch(exist_ok=True)

    @echo.echo
    def on_multiple_events(self, event):
        self.touch_file()
