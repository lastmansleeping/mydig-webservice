import git
from git import Repo
from datetime import datetime
from slacker import Slacker
from config import config

git_push_msg = {64 : 'DELETED', 1024 : 'ERROR', 256 : 'FAST_FORWARD', 128 : 'FORCED_UPDATE',
                2 : 'NEW_HEAD', 1 : 'NEW_TAG', 4 : 'NO_MATCH', 8 : 'REJECTED', 32 : 'REMOTE_FAILURE',
                16 : 'REMOTE_REJECTED', 512 : 'UP_TO_DATE', 1032 : 'REMOTE CONTAINS WORK NOT PRESENT IN LOCAL'}


def push(repo):
    remote_obj = git.Remote(repo,'origin')
    pushinfo = remote_obj.push()
    flags = pushinfo[0].flags
    return flags


def commit(repo, files, commit_message=str(datetime.now())):
    repo.index.add(files)
    repo.index.commit(commit_message)


def pull(repo):
    remote_obj = git.Remote(repo,'origin')
    pullinfo = remote_obj.pull()
    flags = pullinfo[0].flags
    return flags


def execute_command(cmd):
    print 'in execute'
    token = config['slack_auth']['token']
    slack = Slacker(token)

    repo_directory = config['repo_directory']
    repo = Repo(repo_directory)

    if cmd['command'] == 'pull':
        flags = pull(repo)
        return flags

    elif cmd['command'] == 'push':
        flags = push(repo)
        if flags in git_push_msg:
            msg = git_push_msg[flags]
        else:
            msg = 'UNK'
        slack.chat.post_message('#git-sync', 'PUSH - '+str(flags)+' : '+msg)

    elif cmd['command'] == 'commit':
        if 'message' in cmd:
            commit(repo, cmd['files'], cmd['message'])
        else:    
            commit(repo, cmd['files'])

