import requests

# dict_to_send = {'command': 'pull'}
dict_to_send = {'command': 'push'}
# dict_to_send = {'command': 'commit', 'files': ["test22"], 'message': 'added test22'}

if dict_to_send['command'] == 'pull':
    res = requests.post('http://localhost:5000/git-sync', json=dict_to_send)
    print res.content

else:	
    requests.post('http://localhost:5000/git-sync', json=dict_to_send)