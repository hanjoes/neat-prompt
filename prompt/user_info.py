class UserInfo(object):

    def __init__(self, payload):
        self._payload = payload

    def __str__(self):
        return self._payload

    @property
    def payload(self):
        return self._payload