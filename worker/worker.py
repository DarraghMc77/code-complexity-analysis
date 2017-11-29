from pygit2 import Repository, clone_repository, GitError
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
import requests
import json

GIT_REPO_URL = "https://github.com/DarraghMc77/chat-server.git"
GIT_REPO_PATH = "./repo"
API_URL = "127.0.0.1:4000/get_task"
RESPONSE_URL = "127.0.0.1/complexity"


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

def calculate_code_complexity(commit):
    commit_hash = commit['commit']
    index = commit['index']
    print(commit_hash)
    print(index)

def get_commit():
    response = requests.get(API_URL)
    if (response.status_code == 200):
        return json.loads(response.text)
    else:
        print
        "Status Code : %s , Error retrieving data."

def send_cc_result(code_complexity, index):
    json_complexity = json.dumps(code_complexity, sort_keys=True)
    headers = {'content-type': 'application/json'}
    response = requests.post(RESPONSE_URL, data=json_complexity, headers=headers)
    print(response)

def main():
    commit = get_commit()
    calculate_code_complexity(commit)

if __name__ == '__main__':
    main()