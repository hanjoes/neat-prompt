import subprocess
from os import path
from fcntl import lockf, LOCK_EX, LOCK_NB, LOCK_UN

# Files

STATUS_FILE = "/tmp/.neat_prompt_repo_status"
LOCK_FILE = "/tmp/.neat_prompt_lock_file"

# Colors

red = "\[\033[91;1m\]"
green = "\[\033[32;1m\]"
yellow = "\[\033[93;1m\]"
cyan = "\[\033[36;1m\]"
grey = "\[\033[38;2;127;127;127m\]"
reset = "\[\033[0m\]"

# Glyphs

up = red + "\xe2\x86\x91" + reset
cross = red + "\xe2\x9c\x97" + reset
right = "\xe2\x86\x92"
check = green + "\xe2\x9c\x93" + reset
pencil = "\xe2\x9c\x8e"
update = "\xe2\x9c\x89"
question = yellow + "?" + reset

# Quantities

SYNC_INTERVAL = 1


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
