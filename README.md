# Status

![Linting and Unit Tests](https://github.com/hmc-alpaqa/path-complexity/workflows/Lint/badge.svg?branch=develop)

# Developing 

The environment necessary to work on this project is included in 
a docker image. Using docker is highly recommended, as manually 
setting up the environment would involve installing a variety of tools (KLEE, LLVM, JDK, Python, etc.). 

In order to build the image run 

```
make build
```

inside the 'src' directory. Building the image takes a while, so it is also possible to pull an image that is __already built__ from Dockerhub here: 
https://hub.docker.com/repository/docker/gbessler/path_complexity.  

To run the image, do

```
make run
```

inside the 'src' directory. This will put you in a bash shell in the docker image. Note that in this development environment we mount the source code in the host (i.e. the device you are working in) to the docker image. This means that you can modify the code and the changes will me immediately reflected in the docker image. This means it is not necessary to re-build or even re-run the docker image when making code changes. 

Running ```python /app/code/main.py``` in the docker image will put you inside the Path Complexity REPL. This is how the user __usually__ interacts with the tool. Refer to the 'Using the REPL' section to obtain more information about how to use this. 

# Using the Repl

Note that this is essentially a duplicated version of the output obtained from the 'help' command in the REPL. 

### analyze 

Perform statistical analysis on a set of generated metrics. 

Usage: 
analyze <metric names>

### convert 

Convert a file containing source code to a Graph object. 
The recursive flag (-r) can also be used. 

Usage: 
convert <file-like>
convert -r <file-like>
convert <file-like-1> <file-like-2> ... <file-like-n>

### delete 

Delete an object (type Graph, Metrics, or States) from memory. 

Usage: 
delete <type> <name>

### export 

Save an object (type Graph, Metrics, or Stats) to an output file. 

Usage:
save <type> <name>

### list 

List all of the objects of a specific type (either metrics or graphs). 

Usage: 
list <metrics/graphs>
list * 

### metrics 

Compute all of the complexity matrics for a Graph object. 

Usage: 
metrics <name>
metrics * 

### show

Show an object of some type (either metric or graph).

Usage 
show <metric/graph> <name>
show <metric/graph> * 

### quit

Quits the path complexity repl.

## Analyzing Control Flow Graphs

If you would like a pictorial representation of the graphs, it is possible to use the 'export' command to generate '.dot' files. There are many tools to visualize this type of file such as xdot. Running `xdot <file>` will generate an image that can be opened to see the graph.  
