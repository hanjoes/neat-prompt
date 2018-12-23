import getpass
import json
import os
import socket
import time

from prompt.git_info import GitInfo, DOWNLOADING, IN_SYNC, NEWER, OLDER
from prompt.user_info import UserInfo
from util.util import ensure_file_exists, syscmd, STATUS_FILE, SYNC_INTERVAL, \
    syscmd_ub, RED, YELLOW


class Action(object):
    def __init__(self, effect):
        self._effect = effect

    def execute(self):
        return self._effect


class CollectUserInfoAction(Action):
    def execute(self):
        host = CollectUserInfoAction._get_host()
        name = getpass.getuser()
        user_info = UserInfo(name, host)
        user_info.host_color = RED
        user_info.user_name_color = YELLOW
        self._effect.payload = user_info
        return self._effect

    @staticmethod
    def _get_host():
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            return '127.0.0.1'


class CollectGitInfoAction(Action):

    def execute(self):
        self._effect.payload = self._make_git_info()
        return self._effect

    @staticmethod
    def _make_git_info():
        git_info = GitInfo()
        git_info.is_repo = CollectGitInfoAction._is_repo()
        if git_info.is_repo:
            git_info.branch_name = CollectGitInfoAction._get_branch_name()
            git_info.status = CollectGitInfoAction._get_repo_status(git_info.branch_name)
            git_info.changed = CollectGitInfoAction._repo_modified()
        return git_info

    @staticmethod
    def _get_branch_name():
        cmd = ['git', 'symbolic-ref', 'HEAD']
        out = syscmd(cmd)
        refs = out.decode('utf-8').strip().split('/')
        branch = refs[2]
        return branch

    @staticmethod
    def _get_repo_status(branch_name):
        ensure_file_exists(STATUS_FILE)
        with open(STATUS_FILE, "r") as status_file:
            status_json_str = status_file.read()
            stored_status = {} if len(status_json_str) == 0 else json.loads(status_json_str)

            last_sync_time = 0 if status_json_str.isspace() else int(stored_status.get("last_sync_time", "0"))
            cur_time = int(time.time())

            # fetch needed
            if cur_time - last_sync_time >= SYNC_INTERVAL:
                CollectGitInfoAction._keep_in_sync()
                return DOWNLOADING

            return CollectGitInfoAction._resolve_status(branch_name)

    @staticmethod
    def _resolve_status(branch_name):
        try:
            newer = CollectGitInfoAction._local_is_newer(branch_name)
            older = CollectGitInfoAction._local_is_older(branch_name)

            if not newer and not older:
                return IN_SYNC
            elif newer:
                return NEWER
            else:
                return OLDER
        except:
            return OLDER

    @staticmethod
    def _local_is_newer(branch):
        cmd = ['git', 'rev-list', 'origin/' + branch + '..HEAD']
        out = syscmd(cmd)
        if len(out) > 0:
            return True
        return False

    @staticmethod
    def _local_is_older(branch):
        cmd = ['git', 'rev-list', 'HEAD..' + 'origin/' + branch]
        out = syscmd(cmd)
        if len(out) > 0:
            return True
        return False

    @staticmethod
    def _keep_in_sync():
        """
        Asynchronously fetching and updating status file.
        """

        folder = os.path.dirname(os.path.realpath(__file__))
        syscmd_ub(['python', folder + '/fetch_and_update_status.py'])

    @staticmethod
    def _repo_modified():
        cmd = ['git', 'status', '--porcelain']
        res = syscmd(cmd).decode('utf-8')
        l_dirt_status = [entry.split()[0] for entry in [l for l in res.split('\n') if len(l) > 0]]
        modified = False
        if 'M' in l_dirt_status:
            modified = True
        return modified

    @staticmethod
    def _is_repo():
        try:
            syscmd(['git', 'status'])
            return True
        except RuntimeError:
            return False
