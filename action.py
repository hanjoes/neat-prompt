import getpass
import socket

from neat_prompt import syscmd


class Action(object):
    def __init__(self, effect):
        self._effect = effect

    def execute(self):
        return self._effect


class CollectUserInfoAction(Action):

    def execute(self):
        host = CollectUserInfoAction._get_host()
        name = getpass.getuser()
        self._effect.payload = host + "@" + name
        return self._effect

    @staticmethod
    def _get_host():
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            return '127.0.0.1'


class CollectGitInfoAction(Action):

    def execute(self):
        branch_name = CollectGitInfoAction._get_branch_name()
        self._effect.payload = branch_name
        return self._effect

    @staticmethod
    def _get_git_info():
        pass

    @staticmethod
    def _get_branch_name():
        cmd = ['git', 'symbolic-ref', 'HEAD']
        out = syscmd(cmd)
        refs = out.strip().split('/')
        branch = refs[2]
        return branch
