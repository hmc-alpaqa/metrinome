# Metrinome 

![Lint and Test](https://github.com/hmc-alpaqa/metrinome/workflows/Lint%20and%20Test/badge.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![codecov](https://codecov.io/gh/hmc-alpaqa/metrinome/branch/develop/graph/badge.svg)](https://codecov.io/gh/hmc-alpaqa/metrinome)

# Developing 

The environment necessary to work on this project is included in 
a docker image. Using docker is highly recommended, as manually 
setting up the environment would involve installing a variety of tools (KLEE, LLVM, JDK, Python, etc.). 

In order to build the image run 

```
make build
```

inside the 'src' directory. Building the image takes a while, so it is also possible to pull an image that is __already built__ from Dockerhub here: 
https://hub.docker.com/r/harveymudd/metrinome.  
with the command
```
docker pull harveymudd/metrinome
```

To run the image, do

```
make run
```

inside the 'src' directory. This will put you in a shell (zsh by default) in the docker image. Note that in this development environment we mount the source code in the host (i.e. the device you are working in) to the docker image. This means that you can modify the code and the changes will me immediately reflected in the docker image. Therefore, it is not necessary to re-build or even re-run the docker image after making code changes. However, new dependencies will need to be added to the `Dockerfile`, or added to `requirements.txt` if they are Python modules, and the image will then need to be rebuilt with `make build`.

Running 

```
python /app/code/main.py
```

in the docker image will put you inside the Metrinome REPL. This is how the user __usually__ interacts with the tool. Refer to the 'Using the REPL' section to obtain more information about how to use this. The flag *--debug* may be used when running the REPL to get additional information. This will also enable the ```reload``` command. 

The Makefile also contains other useful commands for developing. To run all of the unit tests present in `src/tests/`, use `make test` within the REPL. To execute the linters, use `make check-lint` (or `make lint` to automatically fix common linter issues and then run the linters). Note that this command also runs a typechecker which takes advantage of Python's type hinting feature, so it can help catch errors. It is _*very highly*_ recommended that the linter is executed before any commits are pushed. If pylint makes a recommendation you disagree with, it is possible to disable that pylint check within the section of code you are working in.

## The Codebase

Here are the key components of the repo:

- src/
  - lang_to_cfg/ 
  - metric/
  - core/
  - graph/
  - main.py

The first important component is the src/lang_to_cfg folder. This contains all of the *converters*, which turn code into control flow graphs (CFGs), split per file (e.g. `java.py` knows how to convert Java source code into a graph). The second is the src/metric folder. This contains all of the code for computing complexity metrics from control flow graphs. Another import directory is `core`, which contains the implementation for all of the commands in the REPL. Note that the REPL itself is started with `main.py`, which is a wrapper for `core/command.py`. The utilities for working with klee within the REPL are present in `klee/klee_utils.py`. Another useful directory is `graph`, which contains the Graph and Control Flow Graph objects that Metrinome uses to store results. Many of the files in `src/tests/` are used as examples for unit tests, which also make them great for exploring the features of Metrinome within the REPL.

# Experiments and Data

The C source code for the algorithms used in the KLEE correlational study can be found in `src/tests/cFiles/fse_2020_benchmark/`. Modifications to the code to make it compatible with KLEE (by marking variables as symbolic) and the compiled bytecode files can be found in `src/tests/cFiles/fse_2020_benchmark/kleefiles/`.

Path complexity calculations can only be run inside the REPL. To calculate path complexity for the algorithms in `src/tests/cFiles/fse_2020_benchmark/`, run ```convert /app/code/tests/cFiles/fse_2020_benchmark/filename.c```. This will output a CFG for each function in the file. To look at a list of all generated CFGs, run ```list graphs```. Then, run ```metrics graphname``` to run path complexity on the chosen CFG. To see details on the CFG generated, run ```show graph graphname```, and the edges, nodes, total number of edges and nodes, and source and end nodes will be displayed in text format.

To run Klee from inside the REPL, run ```to_klee_format /app/code/tests/cFiles/fse_2020_benchmark/filename.c``` then ```klee_to_bc filename``` to convert the file to a Klee compatible form then to compile it into bytecode. Finally, run ```klee filename (parameters)``` to actually run Klee. You can see the results with ```show klee_stat filename```.

The script to run the experiment can be found at `src/klee_algs.py`. When inside the docker image, running the script will create Klee compatible files for each of the functions in the `functions` list. For functions that take in arrays, it will set the array size for symbolic execution to `array_size`. It will then run Klee on each of them and record the data for each of the fields in `fields` into a pandas dataframe. It will write the dataframe to a csv in `src/tests/cFiles/fse_2020_benchmark/frames` and create matplotlib plots for each field in `src/tests/cFiles/fse_2020_benchmark/graphs`. The data and graphs for the algorithms in the study is already in those locations.

With higher max-depths, Klee often starts timing out so the paths completed starts dropping or behaving weirdly so the data past this point is not very useful. If you manually find the "breakpoints," you can use `src/analyze_manual.py`to find best fit functions if you also can guess the general functional form (quadratic, exponential, etc). `src/analyze_manual.py` will try to automatically find the breakpoints and the best functional form to fit the data.


# Useful REPL Features

Arrow keys can be used to bring up previous commands. Command history is preserved across REPL sessions (note: sometimes this history is lost if the REPL crashes or we forcefully exit - use the quit command to make sure this does not happen).

# REPL Commands

Note that this is essentially a duplicated version of the output obtained from the 'help' command in the REPL, with some examples thrown in. 

### convert 

Convert a file containing source code to a Graph object. If a directory is passed as an argument, all source
code within that directory will be converted.
The recursive flag (-r) can also be used to convert all files in a given directory *or any of its subdirectories*.

Note - Language Support:

The REPL current supports C/C++ (using clang6), Java (JDK13), and Python 3.
However, only a subset of Python 3 keywords / features are supported: 
assignment, expressions (e.g. 'a + b'), if/else/elif, return, while, and with
(NOTE: this does not include list/dictionary comprehensions, lambda expressions, or try/catch/raise).

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
