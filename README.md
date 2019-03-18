# Running path-complexity in Python

First create a python3 virtual environment and activate it

```
apt-get install python3-virtualenv
virtualenv venv 
source venv/bin/activate 
```

Install the necessary python modules 

```
pip install -r requirements.txt 
```

Run any of the scripts in "scripts-py," e.g. 

```
./simple_tests
```

In order to see the jupyter notebook, run 

```
jupyter notebook 
```

and open 127.0.0.1:8000 in any browser. 

# path-complexity
Path Complexity Analysis 

## Generating Control Flow Graphs

Inside `path-complexity/scripts/cfgextractor` there is a file `main.py` which will run the control flow graph extractor inside of `path-complexity/scripts/cfgextractor/java`.

This will analyze all of the methods in a `.jar` and output their control flow graphs in `.dot` format.

You can run `main.py` by telling it the location of a directory of Java `.jar` files. (It should also work on Java `.class` files.) It requires the full path. For example, on my machine I can run

`> python main.py -i /home/bang/projects/path-complexity/lib_jars/apache_commons/bins/commons-cli-1.2/`

This will generate all of the CFGs for the Apache Commons CLI (command line interface) library methods. 

The source code for `cfgextractor.jar` can be extracted by 'unjar-ing' it. 

## Analyzing Control Flow Graphs

There are some Mathematica files in `path-complexity/src` which compute various complexity metrics on CFGs, read in `.dot` format. 

Rather than running these directly at first, you can try running one of the shell scripts in `path-complexity/scripts` which calls Mathematica's `math` script command, assuming you have `math` installed in `/usr/local/bin/`.

For instance, running `> ./test_run` will analyze 6 CFGs from `/cfgs/simple_test_cfgs` and print out comma-separated stats.

Of course, you can look at the `test_run` file to figure out how to analyze a directory of CGFs from the CGF generation step. 

