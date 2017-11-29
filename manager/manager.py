from pygit2 import Repository, clone_repository, GitError
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
from flask import Flask
import json

GIT_REPO_URL = "https://github.com/KupynOrest/DeblurGAN.git"
GIT_REPO_PATH = "./repo"
commit_list = []
index = 0

app = Flask(__name__)

def get_git_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE):
        commits.append(commit.id)
    return commits

def clone_git_repository():
    repo_url = GIT_REPO_URL
    repo_path = GIT_REPO_PATH
    try:
        repo = Repository(repo_path + '/.git')
    except GitError as e:
        repo = clone_repository(repo_url, repo_path)
        print(repo.head)
    return repo

@app.route("/complexity", methods = ['POST'])
def calculate_complexity():
    global commit_list
    response = "post"
    return response, 200

@app.route("/get_task")
def send_tasks():
    global commit_list
    global index
    if index >= len(commit_list):
        return "No more work", 400
    else:
        response = {'commit': str(commit_list[index]), 'index': index}
        response = json.dumps(response)
        index += 1
        return response, 200

def main():
    repo = clone_git_repository()
    global commit_list
    commit_list = get_git_commits(repo)
    app.run(host='0.0.0.0', port=80, debug=True)

if __name__ == "__main__":
    main()