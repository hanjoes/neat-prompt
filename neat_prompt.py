import getpass
import os
import socket
import subprocess

# Need to add begin and end sequence
# to the non-printable sequences, or
# bash will remove the first prompt
# line.
import time
from os import path

red = '\[\033[91;1m\]'
green = '\[\033[32;1m\]'
yellow = '\[\033[93;1m\]'
cyan = '\[\033[36;1m\]'
grey = '\[\033[38;2;127;127;127m\]'
reset = '\[\033[0m\]'

up = red + '\xe2\x86\x91' + reset
cross = red + '\xe2\x9c\x97' + reset
right = '\xe2\x86\x92'
check = green + '\xe2\x9c\x93' + reset
pencil = '\xe2\x9c\x8e'
update = '\xe2\x9c\x89'

tmp_dir = '/tmp/'

SYNC_INTERVAL = 15

def color_msg(msg, color):
    return color+msg+reset


def local_is_newer(branch):
    cmd = ['git', 'rev-list', 'origin/' + branch + '..HEAD']
    out = syscmd(cmd)
    if len(out) > 0:
        return True
    return False

def local_is_older(branch):
    cmd = ['git', 'rev-list', 'HEAD..' + 'origin/' + branch]
    out = syscmd(cmd)
    if len(out) > 0:
        return True
    return False


def dir_is_repo():
    res = syscmd(['git', 'rev-parse', '--is-inside-work-tree'])
    if res.strip() == 'true':
        return True
    return False


def get_repo_dirty_status():
    cmd = ['git', 'status', '--porcelain']
    res = syscmd(cmd)
    l_dirt_status = [entry.split()[0] for entry in [l for l in res.split('\n') if len(l) > 0]]
    dirty_status = {'modified': False, 'untracked': False}
    if 'M' in l_dirt_status:
        dirty_status['modified'] = True
    return dirty_status


def get_git_status():
    sync_succeeded = fetch_remote()
    is_repo = dir_is_repo()
    branch = None
    is_newer = False
    is_older = False
    dirty_status = None
    if is_repo:
        dirty_status = get_repo_dirty_status()
        branch = get_branch_name()
        is_newer = local_is_newer(branch)
        is_older = local_is_older(branch)
    return {'branch': branch, 'newer': is_newer,
            'older': is_older, 'repo': is_repo,
            'dirty': dirty_status, 'sync': sync_succeeded}


def get_branch_name():
    cmd = ['git', 'symbolic-ref', 'HEAD']
    out = syscmd(cmd)
    refs = out.strip().split('/')
    branch = refs[2]
    return branch


def syscmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if len(err) > 0:
        raise RuntimeError
    return out


def get_host():
    return socket.gethostbyname(socket.gethostname())


def ensure_file_created(filename):
    has_content = False
    if path.isfile(filename):
        fd = open(filename, 'r+')
        if os.stat(filename).st_size > 0:
            has_content = True
    else:
        fd = open(filename, 'w+')
    return fd, has_content


def sync_needed():
    filename = tmp_dir + '.last_fetch_time'
    fd, has_content = ensure_file_created(filename)
    cur_time = int(time.time())
    if has_content:
        for l in fd:
            if cur_time - int(l) > SYNC_INTERVAL:
                fd.seek(0)
                fd.write(str(cur_time))
                return True
    else:
        fd.write(str(cur_time))
        return True
    return False


def fetch_remote():
    if not sync_needed():
        return True
    cmd = ['git', 'fetch']
    try:
        syscmd(cmd)
        return True
    except RuntimeError as e:
        return False


def assemble(name, host, git_status):
    prompt = color_msg(name, yellow) + '@' + color_msg(host, red)
    if not git_status['repo']:
        prompt += color_msg(' (no-repository) ', grey)
        return prompt

    markers = []
    modified = ''
    if git_status['dirty']['modified']:
        modified = '*'
    if git_status['newer']:
        markers.append(up)
        color = cyan
    elif git_status['older']:
        markers.append(cross)
        color = grey
    else:
        markers.append(check)
        color = green
    synced = ''
    if not git_status['sync']:
        synced = '-not-synced'
    prompt += color_msg(' (' + modified + git_status['branch'] + synced + ' ', color)
    prompt += ' '.join(markers)
    prompt += color_msg(') ', color)

    return prompt


def prompt():
    name = getpass.getuser()
    host = get_host()
    try:
        git_status = get_git_status()
    except RuntimeError as e:
        git_status = {'repo': False}
    print assemble(name, host, git_status) + right + ' '

if __name__ == '__main__':
    prompt()
