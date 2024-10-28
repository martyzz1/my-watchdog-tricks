import os
import signal
import subprocess
import time
from pathlib import Path

# Third party libraries
from watchdog.utils import echo

from my_watchdog_tricks.batch import BatchTrick
from my_watchdog_tricks.utils import StreamCaptureCommandOutput


class CheckBeforeAutoRestartTrick(BatchTrick, StreamCaptureCommandOutput):
    """Starts a long-running subprocess and restarts it on matched events.

    The command parameter is a list of command arguments, such as
    ['bin/myserver', '-c', 'etc/myconfig.ini'].

    Call start() after creating the Trick. Call stop() when stopping
    the process.
    """

    def __init__(
        self,
        command,
        check_command,
        patterns=None,
        ignore_patterns=None,
        ignore_directories=False,
        stop_signal=signal.SIGINT,
        kill_after=10,
        autostart=False,
        only_these_events=None,
        touchfile=None,
        source_directory=None,
        files_option=None,  # Optional config for --files option
        **kwargs,
    ):
        self.command = command
        self.check_command = check_command
        self.touchfile = touchfile
        self.only_these_events = only_these_events
        self.stop_signal = stop_signal
        self.kill_after = kill_after
        self.files_option = files_option  # Store the files option config
        self.process = None
        if source_directory:
            self.source_directory = source_directory
        super(CheckBeforeAutoRestartTrick, self).__init__(
            patterns, ignore_patterns, ignore_directories, **kwargs
        )
        if autostart:
            self.start([])  # Start without specific files if autostart

    def check(self, events):
        # print("[{1}] Calling check command - {0}".format(self.check_command, self.command))
        return self.streamcapture(self.check_command)

    def touch_file(self):
        # print("[{1}] Touching - {0}".format(self.touchfile, self.command))
        Path(self.touchfile).touch(exist_ok=True)

    def start(self, files):
        # Append --files argument to self.command if files_option is provided and files are specified
        if self.files_option and files:
            files_argument = self.files_option + " " + " ".join(files)
            self.command.append(files_argument)

        if self.touchfile:
            print(
                "[WATCHMEDO] starting command - {0} with touchfile {1}".format(
                    self.command, self.touchfile
                )
            )
            if self.streamcapture(self.command):
                self.touch_file()
        else:
            print("[WATCHMEDO] starting command - {0}".format(self.command))
            self.process = subprocess.Popen(self.command, preexec_fn=os.setsid)

    def stop(self, files):
        if self.process is None:
            # print("[{0}] Process is None returning instantly".format(self.command))
            return
        print("[WATCHMEDO] stopping command - {0}".format(self.command))
        try:
            os.killpg(os.getpgid(self.process.pid), self.stop_signal)
        except OSError:
            # Process is already gone
            pass
        else:
            kill_time = time.time() + self.kill_after
            while time.time() < kill_time:
                if self.process.poll() is not None:
                    break
                time.sleep(0.25)
            else:
                try:
                    os.killpg(os.getpgid(self.process.pid), 9)
                except OSError:
                    # Process is already gone
                    pass
        self.process = None

    @echo.echo
    def on_multiple_events(self, events):
        # Filter and collect src_path values based on event type
        if self.only_these_events:
            files = [
                event.src_path
                for event in events
                if event.event_type in self.only_these_events
            ]
        else:
            files = [event.src_path for event in events]

        # Deduplicate files list
        files = list(set(files))

        # Proceed if there are valid events and check is successful
        if files and self.check(events):
            self.stop(files)
            self.start(files)
        else:
            print("No valid events were received")
