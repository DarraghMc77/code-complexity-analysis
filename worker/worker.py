from pygit2 import Repository, clone_repository, GitError
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
import requests
import json
import sys
from radon.complexity import cc_visit
import time

GIT_REPO_URL = 'https://github.com/KupynOrest/DeblurGAN.git'
GIT_REPO_PATH = './repo'
API_URL = 'http://10.6.69.232:4008/get_task'
RESPONSE_URL = 'http://10.6.69.232:4008/complexity'

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
def extract_python_files(repo, directory):
    python_files = []
    for file in directory:
        if file.type == 'tree':
            python_files += extract_python_files(repo, repo[file.id])
        elif file.name.endswith('.py'):
            python_files.append(file)
    return python_files

def clone_git_repository():
    try:
        repo = Repository(GIT_REPO_PATH + '/.git')
    except GitError as e:
        print("Cloning Repository")
        repo = clone_repository(GIT_REPO_URL, GIT_REPO_PATH)
    return repo

def calculate_code_complexity(commit):
    commit_hash = commit['commit']
    index = commit['index']
    print(commit_hash)
    print(index)

def send_cc_result(code_complexity, index):
    cc_result = {'complexity': code_complexity, 'index': index}
    json_complexity = json.dumps(cc_result)
    headers = {'content-type': 'application/json'}
    response = requests.post(RESPONSE_URL, data=json_complexity, headers=headers)
    print(response)

def get_commit():
    response = requests.get(API_URL)
    if (response.status_code == 200):
        return json.loads(response.text)
    elif(response.status_code == 400):
        print("Work Complete")
        sys.exit()

def main():
    repo = clone_git_repository()
    print("Repository Cloned")
    while True:
        try:
            data = get_commit()
            commit = data['commit']
            index = data['index']
        except ValueError:
            time.sleep(30)
            continue
        commit_obj = repo.get(commit)
        python_files = extract_python_files(repo, commit_obj.tree)

        complexity_result = 0

        for file in python_files:
            complexity_result += calculate_obj_complexity(repo[file.id].data)

        send_cc_result(complexity_result, index)

if __name__ == '__main__':
    main()