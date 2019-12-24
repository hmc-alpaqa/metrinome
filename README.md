# Developing 

The environment necessary to work on this project is included in 
a docker image. Using docker is highly recommended, as manually 
setting up the environment would involve installing a variety of tools (KLEE, LLVM, JDK, Python, etc.). 

In order to build the image run 

```
docker build -f <path_to_Dockerfile.dev> .
```

Now run ```docker images```. Obtain the "IMAGE ID" for the image you just created. This will look something like 'd3cb9c11dded'. 
Then to run the image use

```
docker run -it -v <path_to path-complexity/src>:/app/code <image_ID> /bin/bash
```

This will put you in a bash shell in the docker image. Not that in this development environment we mount the source code in the host (i.e. the device you are working in) to the docker image. This means that you can modify the code and the changes will me immediately reflected in the docker image. This means it is not necessary to re-build or even re-run the docker image when making code changes.

Running ```python /app/code/main.py``` in the docker image will put you inside the Path Complexity REPL. This is how the user __usually__ interacts with the tool. Refer to the 'Using the REPL' section to obtain more information about how to use this. 

# Using the Repl

Note that this is essentially a duplicated version of the output obtained from the 'help' command in the REPL. 

### analyze 

### convert 

### delete 

### export 

### list 

### metrics 

### show

## Analyzing Control Flow Graphs

If you would like a pictorial representation of the graphs, it is possible to use the 'export' command to generate '.dot' files. There are many tools to visualize this type of file such as xdot. Running `xdot <file>` will generate an image that can be opened to see the graph.  