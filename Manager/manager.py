from pygit2 import Repository, clone_repository, GitError
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
from flask import Flask

GIT_REPO_URL = "https://github.com/DarraghMc77/chat-server.git"
GIT_REPO_PATH = "./repo"
commit_list = []

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

@app.route("/get_task")
def hello():
    global commit_list
    print(commit_list)
    return commit_list[0]

def main():
    repo = clone_git_repository()
    commit_list = get_git_commits(repo)
    print(commit_list)
    app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    main()