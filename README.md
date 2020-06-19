# Metrinome 

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
https://hub.docker.com/repository/docker/gbessler/pathrepl.  
with the command
```
docker pull gbessler/pathrepl
```

To run the image, do

```
make run
```

inside the 'src' directory. This will put you in a shell (zsh by default) in the docker image. Note that in this development environment we mount the source code in the host (i.e. the device you are working in) to the docker image. This means that you can modify the code and the changes will me immediately reflected in the docker image. Therefore, it is not necessary to re-build or even re-run the docker image after making code changes. However, new dependencies will need to be added to the `Dockerfile`, or added to `requirements.txt` if they are Python modules.

Running 

```
python /app/code/main.py
```

in the docker image will put you inside the Path Complexity REPL. This is how the user __usually__ interacts with the tool. Refer to the 'Using the REPL' section to obtain more information about how to use this. The flag *--debug* may be used when running the REPL to get additional information. This will also enable the ```reload``` command. 

The Makefile also contains other useful commands for developing. To run all of the unit tests present in `src/tests/`, use `make tests` within the REPL. To execute the linters, use `make lint`. Note that this command also runs a typechecker which takes advantage of Python's type hinting feature, so it can help catch errors. It is _*very highly*_ recommended that the linter is executed before any commits are pushed. If pylint makes a recommendation you disagree with, it is possible to disable that pylint check within the section of code you are working in.

## The Codebase

Here are the key components of the repo:

- src/
  - lang_to_cfg/ 
  - metric/
  - command.py
  - main.py
  - klee_utils.py
  - graph.py

The first important component is the src/lang_to_cfg folder. This contains all of the *converters*, which turn code into control flow graphs (CFGs), split per file (e.g. `java.py` knows how to convert Java source code into a graph). The second is the src/metric folder. This contains all of the code for computing complexity metrics from control flow graphs. The other most important file is `command.py`, which contains the implementation for all of the commands in the REPL. Note that the REPL itself is started with `main.py`, which is a wrapper for `command.py`. The utilities for working with klee within the REPL are present in `klee_utils.py`. Another useful file is `graph.py`, which contains the Graph object that Metrinome uses to store. Many of the files in `src/tests/` are used as examples for unit tests, which also make them great for exploring the features of Metrinome within the REPL.

# Experiments and Data

The C source code for the algorithms used in the KLEE correlational study can be found in `src/tests/cFiles/simpleAlgs/`. The modification of this code to make it compatible with KLEE (by marking variables as symbolic) can be found in `src/tests/cFiles/simpleAlgs/kleeFiles/`. 

# Useful REPL Features

Arrow keys can be used to bring up previous commands. Command history is preserved across REPL sessions (note: sometimes this history is lost if the REPL crashes or we forcefully exit - use the quit command to make sure this does not happen).

# REPL Commands

Note that this is essentially a duplicated version of the output obtained from the 'help' command in the REPL, with some examples thrown in. 

### convert 

Convert a file containing source code to a Graph object. If a directory is passed as an argument, all source
code within that directory will be converted.
The recursive flag (-r) can also be used to convert all files in a given directory *or any of its subdirectories*.

Usage: 
convert \<file-like>
  
convert -r \<file-like>
  
convert \<file-like-1> \<file-like-2> ... \<file-like-n>

### delete 

Delete an object (type graph, metric, or klee_stat, klee_bc, klee_file, or klee) from memory. 
The wildcard operator * is also supported for 'type'.
Using the klee type deletes all klee-related objects with that name.

Usage: 
delete \<type> \<name>

### import

Import a .dot graph file as a graph object. Similar to `convert`, if a directory
of .dot files is passed as an argument, all graphs will be imported. 
The recursive flag (-r) can also be used to import all graphs from a directory
and subdirectories.

Usage: 
import \<file-like>
  
import -r \<file-like>
  
import \<file-like-1> \<file-like-2> ... \<file-like-n>

### export 

Save an object (type graph, metric, klee_bc, klee_file, or klee) to an output file.
Using type klee exports all klee-related objects with that name.

Usage:
export \<type> \<name>

### list 

List all of the objects of a specific type (metric, graph, klee_bc, klee_stat, klee_file, or klee).
The wildcard operator * is also supported for type.
Using the klee type lists all klee-related objects - organized by type.

Usage: 
list \<type>

### metrics 

Compute all of the complexity matrics for a Graph object. This currently computes
Cyclomatic Complexity, NPath Complexity, and Path Complexity / Asymptotic Path Complexity.
The wildcard operator * is supported for names.

Usage: 
metrics \<name>

### reload

Reloads command definitions in the module (only works in debug mode) while presenting objects in the REPL. This is an easy way to verify that a change to a command works without having to restart the REPL (causing all objects to be deleted). 

Usage:
reload

### show

Print out a representation of an object of some type (metric, graph, klee_bc, klee_file, klee_stat, or klee).
The wildcard operator * is spported for type and name.
Type klee will show all klee-related objects with the given name.
The object names can be obtained with `list`.

Usage:
show \<type> \<name>

### quit

Quits the path complexity repl. This is the recommended way to exit as it guaranteeds that the command history will be 
preserved for the next time the REPL is executed.

## Working With KLEE

Before KLEE can be executed on C source code, we must specify which variables are *symbolic* and which functions we want to test.
While this process can be done manually, which may give users more granular control of KLEE behavior, the klee utilities in the REPL
cover general use cases. The command `to_klee_format` looks through C source files, finds all function definitions, and creates a new
source file that contains `main()`, which marks of the arguments in the original function definitions as symbolic and then calls those 
functions. Functions that take user input may need to be refactored. Further, functions that rely on imports must be dealt with more carefully -
i.e. ensure that KLEE can find all of the required files by adding the appropriate paths and fake headers to the path environment variable.

Once in this format, call `klee_to_bc` to convert this modified C source into a `.bc` file. Then, call `klee` on the output from the previous command.

### to_klee_format 

Create a klee-compatible file.

Given a C file, create a new modified C file that is in the correct format to be converted to a bc file.

### klee_to_bc 

Given a C file in the correct format, generate a new .bc file from the given C file.

### klee_replay

Execute a test generated by KLEE given a klee test file.

Usage:
klee_replay <file>
  
### klee

Execute the klee command on a .bc file.

This will generate all of the tests automatically and store the resulting metadata (e.g. number of tests generated).

Usage:
klee <file>

## Navigating Within the REPL

Many of the basic commands used for navigating around files in typical shells also work in the REPL. We currently support `cd`, `ls`, `mv`, `rm`, `mkdir`, and `pwd`. 

# Analyzing Control Flow Graphs

If you would like a pictorial representation of the graphs, it is possible to use the 'export' command to generate '.dot' files. There are many tools to visualize this type of file such as xdot. Running `xdot <file>` will generate an image that can be opened to see the graph. GraphvizOnline is another great tool to easily visualize and modify these graphs.
