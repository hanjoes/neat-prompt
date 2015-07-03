import getpass
import socket
import subprocess

# Need to add begin and end sequence
# to the non-printable sequences, or
# bash will remove the first prompt
# line.
red = '\[\033[91;1m\]'
green = '\[\033[32;1m\]'
yellow = '\[\033[93;1m\]'
cyan = '\[\033[36;1m\]'
grey = '\[\033[37;1m\]'
reset = '\[\033[0m\]'

up = '\xe2\x86\x91'
down = '\xe2\x86\x93'
right = '\xe2\x86\x92'
check = '\xe2\x9c\x93'

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
    # fatal: Not a git repository (or any of the parent directories): .git
    res = syscmd(['git','rev-parse','--show-toplevel'])
    lines = [line for line in res.split('\n') if len(line)>0]
    if 'fatal' in lines[0]:
        return False
    return True


def get_git_status():
    is_repo = dir_is_repo()
    branch = ''
    is_newer = False
    is_older = False
    if is_repo:
        branch = get_branch_name()
        is_newer = local_is_newer(branch)
        is_older = local_is_older(branch)
    return {'branch': branch, 'newer': is_newer, 'older': is_older, 'repo': is_repo}


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


def assemble(name, host, git_status):
    prompt = color_msg(name, yellow) + '@' + color_msg(host, red)
    if not git_status['repo']:
        prompt += color_msg(' (no-repository) ', grey)
        return prompt

    if git_status['newer']:
        prompt += color_msg(' (' + git_status['branch'] + ' ' + up + ') ', cyan)
    elif git_status['older']:
        prompt += color_msg(' (' + git_status['branch'] + ' ' + down + ') ', red)
    else:
        prompt += color_msg(' (' + git_status['branch'] + ' ' + check + ') ', green)
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