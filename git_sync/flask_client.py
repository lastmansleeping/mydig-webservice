import requests
import config


# Have to pass the User credentials in the request. - Username and Oauth_token.

# Git Commands - Push, Pull, Commit
#dict_to_send = {'command': 'pull'}
dict_to_send = {'command': 'push'}
#dict_to_send = {'command': 'commit', 'files': ["test26"], 'message': 'added test26'}

if dict_to_send['command'] == 'pull':
    res = requests.post('http://localhost:5000/git-sync', json=dict_to_send)
    print res.content

else:
    requests.post('http://localhost:5000/git-sync', json=dict_to_send)
