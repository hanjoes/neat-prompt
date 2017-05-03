import subprocess
from os import path
from fcntl import lockf, LOCK_EX, LOCK_NB, LOCK_UN


STATUS_FILE = "/tmp/.neat_prompt_repo_status"
SYNC_INTERVAL = 1
LOCK_FILE = "/tmp/.neat_prompt_lock_file"


def ensure_file_exists(file_name):
    if not path.isfile(file_name):
        with open(file_name, "w") as _:
            pass


def acquire_file_lock(lock_file):
    with open(lock_file, "w") as fd:
        lockf(fd, LOCK_EX | LOCK_NB)


def release_file_lock(lock_file):
    with open(lock_file, "w") as fd:
        lockf(fd, LOCK_UN)


def syscmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if len(err) > 0:
        raise RuntimeError
    return out


def syscmd_ub(cmd):
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
