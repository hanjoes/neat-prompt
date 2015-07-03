import getpass
import socket
import subprocess

red = '\033[31;1m'
green = '\033[32;1m'
yellow = '\033[33;1m'
cyan = '\033[36;1m'
reset = '\033[0m'

up = '\xe2\x86\x91'
down = '\xe2\x86\x93'
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


def get_git_status():
    branch = get_branch_name()
    is_newer = local_is_newer(branch)
    is_older = local_is_older(branch)
    return {'branch': branch, 'newer': is_newer, 'older': is_older}


def get_branch_name():
    cmd = ['git', 'symbolic-ref', 'HEAD']
    out = syscmd(cmd)
    refs = out.strip().split('/')
    branch = refs[2]
    return branch


def syscmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out


def get_host():
    return socket.gethostbyname(socket.gethostname())


def assemble(name, host, git_status):
    prompt = color_msg(name, yellow) + '@' + color_msg(host, red)
    if git_status['newer']:
        prompt += ' ' + color_msg(git_status['branch'] + ' ' + up, cyan)
    elif git_status['older']:
        prompt += ' ' + color_msg(git_status['branch'] + ' ' + down, red)
    else:
        prompt += ' ' + color_msg(git_status['branch'] + ' ' + check, green)
    return prompt


def prompt():
    name = getpass.getuser()
    host = get_host()
    git_status = get_git_status()
    print assemble(name, host, git_status)

if __name__ == '__main__':
    prompt()