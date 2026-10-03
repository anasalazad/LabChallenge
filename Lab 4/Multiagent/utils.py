import sys
import threading

LOG_LEVEL = "INFO"
TIMEOUT = 60


class thread_with_trace(threading.Thread):

    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        self._return = None

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def run(self):
        if self._target is not None:
            self._return = self._target(
                *self._args,
                **self._kwargs
            )

    def globaltrace(self, frame, event, arg):
        if event == "call":
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == "line":
                raise SystemExit()

        return self.localtrace

    def kill(self):
        self.killed = True

    def join(self, timeout=0):
        threading.Thread.join(self, timeout)
        return self._return
