# CS7NS1 - REST Service Development Task
Assignment for CS7NS1 in which a master-slave architecture is employed to calculate cyclomatic complexity of every commit in a github repository.

This assignment was implemented with the use of a manager which distributes work to a set of worker nodes. The worker nodes use the work stealing pattern to ask for work. This is done by sending a GET request to the manager. The manager then sends the hash of the commit that the worker then uses to calculate the cyclomatic complexity of that particular commit. The result of this cyclomatic complexity is then sent to the manager using a POST request. When the manager receives a result for every commit, the results are then graphed 

## How to run
To build 
```
docker-compose build
```
To run
```
docker-compose up
```

## Results
### Cyclomatic Complexity Results

![alt text](https://github.com/DarraghMc77/code-complexity-analysis/blob/master/manager/graph.png)

### Time Taken Per Number of Slave Nodes(seconds)
* 1 Node - 3.530900239944458
* 2 Nodes - 2.0651612281799316
* 3 Nodes - 2.021984758377075
* 4 Nodes - 1.7649774551391602
* 5 Nodes - 1.7970986366271973
