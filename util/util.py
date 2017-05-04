import subprocess
from os import path
from fcntl import lockf, LOCK_EX, LOCK_NB, LOCK_UN

# Files

STATUS_FILE = "/tmp/.neat_prompt_repo_status"
LOCK_FILE = "/tmp/.neat_prompt_lock_file"

# Colors

RED = "\[\033[91;1m\]"
GREEN = "\[\033[32;1m\]"
YELLOW = "\[\033[93;1m\]"
CYAN = "\[\033[36;1m\]"
GREY = "\[\033[38;2;127;127;127m\]"
RESET = "\[\033[0m\]"

# Glyphs

UP = RED + "\xe2\x86\x91" + RESET
CROSS = RED + "\xe2\x9c\x97" + RESET
RIGHT = "\xe2\x86\x92"
CHECK = GREEN + "\xe2\x9c\x93" + RESET
QUESTION = YELLOW + "?" + RESET

# Quantities

SYNC_INTERVAL = 10


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
        raise RuntimeError(err)
    return out


def syscmd_ub(cmd):
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def enclose_in_color(s, color):
    return color + s + RESET
