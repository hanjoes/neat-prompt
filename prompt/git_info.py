# ------------------------------
# CONSTANTS

NO_REPO = "no-repository"
FAILED = "failed"
# ------------------------------

# ------------------------------
# STATUS

NEWER = 1
OLDER = 2
IN_SYNC = 3
DOWNLOADING = 4
DISCONNECTED = 5
# ------------------------------


class GitInfo(object):

    def __init__(self):
        self._branch_name = NO_REPO
        self._changed = False
        self._msg = ""
        self._status = None

    def __str__(self):
        changed_mark = "*" if self._changed else ""
        return "({}{} {}{})".format(changed_mark, self._branch_name, str(self._status), self._msg)

    @property
    def branch_name(self):
        return self._branch_name

    @branch_name.setter
    def branch_name(self, b):
        self._branch_name = b

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, c):
        self._changed = c

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, m):
        self._msg = m

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s):
        self._status = s
