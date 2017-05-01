class Prompt(object):
    def __init__(self):
        self._user_str = ""
        self._git_str = ""

    def __str__(self):
        return self._user_str + " " + self._git_str

    @property
    def user_str(self):
        return self._user_str

    @user_str.setter
    def user_str(self, s):
        self._user_str = s

    @property
    def git_str(self):
        return self._git_str

    @git_str.setter
    def git_str(self, s):
        self._git_str = s
