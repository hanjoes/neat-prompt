# ------------------------------
# CONSTANTS
from util.util import CYAN, UP, GREY, CROSS, GREEN, CHECK, YELLOW, QUESTION, RESET

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

# Map from status -> (branch_color, symbol, message)
STATUS_VISUAL_MAP = {
    NEWER: (CYAN, UP, ""),
    OLDER: (GREY, CROSS, ""),
    IN_SYNC: (GREEN, CHECK, ""),
    DOWNLOADING: (YELLOW, QUESTION, ""),
    DISCONNECTED: (GREY, CROSS, ""),
    NO_REPO: (GREY, "", "")
}


class GitInfo(object):

    def __init__(self):
        self._is_repo = True
        self._branch_name = NO_REPO
        self._changed = False
        self._msg = ""
        self._status = None

    def __str__(self):
        if self.is_repo:
            changed_mark = "*" if self._changed else ""
            branch_color = STATUS_VISUAL_MAP[self.status][0]
            symbol = STATUS_VISUAL_MAP[self.status][1]
            return "{0}({2}{3}{1} {4}{0}{5}){1}"\
                .format(branch_color, RESET, changed_mark, self.branch_name, symbol, self.msg)
        else:
            return "{0}(no_repository){1}".format(GREY, RESET)

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

    @property
    def is_repo(self):
        return self._is_repo

    @is_repo.setter
    def is_repo(self, b):
        self._is_repo = b
