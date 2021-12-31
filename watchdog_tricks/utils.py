from subprocess import Popen, PIPE, STDOUT


class StreamCaptureCommandOutput():

    def streamcapture(self, command):

        print("[WATCHMEDO] Starting for {0}".format(command))
        with Popen(command, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                print("[WATCHMEDO] {0}".format(line), end='')  # process line here

        print("[WATCHMEDO] Finished for {0}".format(command))
        if p.returncode != 0:
            return 0
        return 1
