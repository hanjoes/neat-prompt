class UserInfo(object):

    def __init__(self, payload):
        self._payload = payload

    @property
    def payload(self):
        return self._payload