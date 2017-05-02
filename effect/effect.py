class Effect(object):
    def __init__(self):
        self._payload = None

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, p):
        self._payload = p

    def apply_to(self, prompt):
        raise NotImplementedError


class SetUserInfoEffect(Effect):

    def apply_to(self, prompt):
        prompt.user_info = self._payload


class SetGitInfoEffect(Effect):

    def apply_to(self, prompt):
        prompt._git_info = self._payload
