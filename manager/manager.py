from __future__ import print_function
from pygit2 import Repository, clone_repository, GitError
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
from flask import Flask, request
import matplotlib
import json
import sys
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GIT_REPO_URL = "https://github.com/KupynOrest/DeblurGAN.git"
GIT_REPO_PATH = "./repo"
commit_list = []
complexity_results = []
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

def graph_results(complexity_results):
    print("Final Results", file=sys.stderr)
    print(complexity_results, file=sys.stderr)
    f, ax = plt.subplots(1)
    xdata = range(len(complexity_results))
    ydata = complexity_results
    plt.ylabel('Complexity')
    plt.xlabel('Commit')
    ax.plot(xdata, ydata)
    ax.set_ylim(ymin=0)
    plt.show()
    plt.savefig("graph.png")

@app.route("/complexity", methods = ['POST'])
def calculate_complexity():
    global complexity_results
    global commit_list
    json_complexity = request.get_json()
    index = json_complexity['index']
    complexity = json_complexity['complexity']
    print(index, file=sys.stderr)
    print(complexity, file=sys.stderr)
    complexity_results[index] = complexity
    if(len(complexity_results) >= len(commit_list)):
        graph_results(complexity_results)
    print(complexity_results, file=sys.stderr)
    response = request.get_json()
    return json_complexity, 200

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
    global complexity_results
    commit_list = get_git_commits(repo)
    complexity_results = [0] * len(commit_list)
    app.run(host='0.0.0.0', port=80, debug=True)

if __name__ == "__main__":
    main()