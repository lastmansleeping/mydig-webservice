from flask import Flask
from flask import request
import git_sync
from config import config
import multiprocessing

app = Flask(__name__)

git_pull_msg = {128: "ERROR", 64: "FAST_FORWARD", 32: "FORCED_UPDATE", 4: "HEAD_UPTODATE",
                2: "NEW_HEAD", 1: "NEW_TAG", 16: "REJECTED", 8: "TAG_UPDATE"}


@app.route("/git-sync", methods=['POST'])
def git_synchronization():
    cmd = request.get_json()
    if cmd['command'] == 'pull':
        return_message = git_sync.execute_command(cmd)
        json_reply = {}
        if return_message == 64:
            json_reply['return_code'] = 0
        else:
            json_reply['return_code'] = return_message
            json_reply['error_message'] = git_pull_msg[return_message]
        return str(json_reply)
    else:
        p = multiprocessing.Process(target=git_sync.execute_command, args = (cmd,))
        p.start()
        return str(1)
 
if __name__ == "__main__":
    app.run(host=config['flask_server']['host'], port=config['flask_server']['port'])