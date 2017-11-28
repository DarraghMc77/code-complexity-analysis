import config
from pygit2 import Repository, clone_repository
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE

def get_git_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE):
        commits.append(commit.id)
    return commits

def do_clone_repository():
    repo_url = 'https://github.com/DarraghMc77/chat-server.git'
    repo_path = '/Users/Darragh/College/ScalableComputing/code-complexity-analysis/chat-server'
    repo = clone_repository(repo_url, repo_path)
    return repo

def main():
    repo = do_clone_repository()
    print(get_git_commits(repo))

if __name__ == '__main__':
    main()