class Prompt(object):
    def __init__(self):
        self._user_info = None
        self._git_info = None

    def __str__(self):
        return str(self._user_info) + " " + str(self._git_info)

    @property
    def user_info(self):
        return self._user_info

    @user_info.setter
    def user_info(self, s):
        self._user_info = s

    @property
    def git_info(self):
        return self._git_info

    @git_info.setter
    def git_info(self, s):
        self._git_info = s
