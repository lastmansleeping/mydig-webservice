import git
from git import Repo
from datetime import datetime
from slacker import Slacker
from config import config

git_push_msg = {64 : 'DELETED', 1024 : 'ERROR', 256 : 'FAST_FORWARD', 128 : 'FORCED_UPDATE',
                2 : 'NEW_HEAD', 1 : 'NEW_TAG', 4 : 'NO_MATCH', 8 : 'REJECTED', 32 : 'REMOTE_FAILURE',
                16 : 'REMOTE_REJECTED', 512 : 'UP_TO_DATE', 1032 : 'REMOTE CONTAINS WORK NOT PRESENT IN LOCAL'}


def push(remote_obj):
    pushinfo = remote_obj.push()
    flags = pushinfo[0].flags
    return flags


def commit(repo, files, commit_message=str(datetime.now())):
    repo.index.add(files)
    repo.index.commit(commit_message)


def pull(remote_obj):
    pullinfo = remote_obj.pull()
    flags = pullinfo[0].flags
    return flags


def execute_command(cmd):

    token = config['slack']['slack_auth']['token']
    slack = Slacker(token)

    repo_directory = config['repo_directory']
    repo = Repo(repo_directory)
    remote_obj = git.Remote(repo,'origin')

    url = remote_obj.url.split('@')[1]
    auth_url = 'https://{}:{}@'.format(cmd['user_credentials']['username'], cmd['user_credentials']['oauth_token']) + url

    remote_obj.set_url(auth_url)

    if cmd['command'] == 'pull':
        flags = pull(remote_obj)
        return flags

    elif cmd['command'] == 'push':
        flags = push(remote_obj)
        if flags in git_push_msg:
            msg = git_push_msg[flags]
        else:
            msg = 'UNK'
        slack.chat.post_message(config['slack']['slack_channel'], 'PUSH - '+str(flags)+' : '+msg)

    elif cmd['command'] == 'commit':
        if 'message' in cmd:
            commit(repo, cmd['files'], cmd['message'])
        else:    
            commit(repo, cmd['files'])
