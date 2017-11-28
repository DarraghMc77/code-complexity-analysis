import config
from pygit2 import Repository, clone_repository, GitError
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE

def get_git_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE):
        commits.append(commit.id)
    return commits

def clone_git_repository():
    repo_url = config.GIT_REPO_URL
    repo_path = config.GIT_REPO_PATH
    try:
        repo = Repository(repo_path + '/.git')
    except GitError as e:
        repo = clone_repository(repo_url, repo_path)
    return repo

def main():
    repo = clone_git_repository()
    print(get_git_commits(repo))

if __name__ == '__main__':
    main()