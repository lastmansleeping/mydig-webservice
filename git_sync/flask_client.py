import requests
import config


# Have to pass the User credentials in the request. - Username and Oauth_token.

# Git Commands - Push, Pull, Commit
#dict_to_send = {'command': 'pull'}
dict_to_send = {'command': 'push'}
#dict_to_send = {'command': 'commit', 'files': ["test25"], 'message': 'added test25'}

# User credentials format - 
# dict_to_send['user_credentials'] = {'username':'<Username>', 'oauth_token': '<Oauth Token>'}
dict_to_send['user_credentials'] = {'username':'Dhvanan', 'oauth_token': '20d2da0882252c35d4a758779152daef3544d651'}

if dict_to_send['command'] == 'pull':
    res = requests.post('http://localhost:5000/git-sync', json=dict_to_send)
    print res.content

else:
    requests.post('http://localhost:5000/git-sync', json=dict_to_send)
