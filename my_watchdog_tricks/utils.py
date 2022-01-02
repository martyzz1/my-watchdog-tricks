import os
import sys
from functools import wraps
from glob import glob
from subprocess import PIPE, STDOUT, Popen


def trace_event(func):
    @wraps(func)
    def _traced_func(self, event):
        if hasattr(event, "dest_path"):
            print("{0}: {1} -> {2}".format(event.event_type, event.src_path, event.dest_path))
        else:
            print("{0} {1}".format(event.event_type, event.src_path))
        return func(self, event)

    return _traced_func


def exec_cmd(cmd, echo=True):
    if echo:
        sys.stdout.write("Execute command: %s\n" % cmd)
        sys.stdout.flush()
    process = Popen(cmd, shell=True)
    process.wait()


def build_tags(basedir, filetypes, ctags="ctags", recursive=False):
    olddir = os.getcwd()
    os.chdir(basedir)
    files = sum([glob("*." + ftype) for ftype in filetypes], [])
    if files:
        print("Generate tags for {0} file(s) in {1}".format(len(files), basedir))
        ctags_cmd = "%s %s" % (ctags, " ".join(files))
        exec_cmd(ctags_cmd, echo=False)
    if recursive:
        for root, dirs, files in os.walk(basedir):
            for d in dirs:
                build_tags(os.path.join(root, d), filetypes, ctags, recursive)
    os.chdir(olddir)


class StreamCaptureCommandOutput:
    def streamcapture(self, command):

        print("[WATCHMEDO] Starting for {0}".format(command))
        with Popen(command, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                print("[WATCHMEDO] {0}".format(line), end="")  # process line here

        print("[WATCHMEDO] Finished for {0}".format(command))
        if p.returncode != 0:
            return 0
        return 1
