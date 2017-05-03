from neat_prompt import reset


class UserInfo(object):
    def __init__(self, user_name, host):
        self._user_name = user_name
        self._host = host
        self._user_name_color = None
        self._host_color = None

    def __str__(self):
        return self._user_name + "@" + self._host

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, u):
        self._user_name = u

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, h):
        self._host = h

    @property
    def user_name_color(self):
        return self._user_name_color

    @user_name_color.setter
    def user_name_color(self, c):
        self._user_name_color = c

    @property
    def host_color(self):
        return self._host_color

    @user_name_color.setter
    def user_name_color(self, c):
        self._host_color = c
