from pygit2 import Repository, clone_repository, GitError
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
import requests
import json
import sys
from radon.complexity import cc_visit

GIT_REPO_URL = "https://github.com/KupynOrest/DeblurGAN.git"
GIT_REPO_PATH = "./repo"
API_URL = "http://10.6.92.89:4007/get_task"
RESPONSE_URL = "http://10.6.92.89:4007/complexity"

def calculate_obj_complexity(filetext):
    complexities = []
    try:
        complexity_objs = cc_visit(filetext)
        for obj in complexity_objs:
            complexities.append(obj.complexity)
        return sum(complexities)
    except Exception:
        return 0.0

# Needs fixing
def calculate_cyclomatic_complexity(repo, directory, complexity_result):
    python_files = []
    for file in directory:
        if file.type == 'tree':
            complexity_result += calculate_cyclomatic_complexity(repo, repo[file.id], complexity_result)
        elif file.name.endswith('.py'):
            python_files.append(file)
            complexity_result += calculate_obj_complexity(repo[file.id].data)
    return complexity_result

def clone_git_repository():
    try:
        repo = Repository(GIT_REPO_PATH + '/.git')
    except GitError as e:
        repo = clone_repository(GIT_REPO_URL, GIT_REPO_PATH)
        print(repo.head)
    return repo

def calculate_code_complexity(commit):
    commit_hash = commit['commit']
    index = commit['index']
    print(commit_hash)
    print(index)

def send_cc_result(code_complexity, index):
    json_complexity = json.dumps(code_complexity, sort_keys=True)
    headers = {'content-type': 'application/json'}
    response = requests.post(RESPONSE_URL, data=json_complexity, headers=headers)
    print(response)

def get_commit():
    response = requests.get(API_URL)
    if (response.status_code == 200):
        return json.loads(response.text)['commit']
    elif(response.status_code == 400):
        print("Work Complete")
        sys.exit()

def main():
    repo = clone_git_repository()
    commit = get_commit()
    commit_obj = repo.get(commit)
    total_complexity = calculate_cyclomatic_complexity(repo, commit_obj.tree, 0.0)
    print(total_complexity)

if __name__ == '__main__':
    main()