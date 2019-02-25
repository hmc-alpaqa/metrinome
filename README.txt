Quick start:

  Navigate to src. 
  Run ./simple_tests to get a quick idea of how things work. 
  This processes the example control flow graphs in 
     cfgs/simple_test_cfgs. 
  Output is saved to 
     results/simple_test_results.csv.
  You can view the results in LibreOffice.
     You may have to adjust column width.

  To view a CFG file you can run xdot. Try the following: 

  xdot ~/PathComplexity/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test4_0_basic.dot 

=====================================
More detailed instructions.

Directory Contents:

---------------------
scripts: 
---------------------  

Contains 6 scripts for demonstrating computation of path complexity, cyclomatic complexity, and NPATH complexity. Also contains for a sub directory 'cfgextractor' for control-flow graph generation.

Output of all scripts contains 
	- testnumber
	- filename
	- cyclomatic complexity 
	- npath complexity
	- path complexity classification:
          Constant, Polynomial, or Exponential
	- path counting function
	- asymptotic complexity 

1. complexites: 

Computes results for a single cfg file or entire directory and outputs a line of comma separated results to sdtout for each file.

	usage:  ./complexities /path/to/cfg/file
		./complexities /path/to/cfg/directory

	output: stdout


2. simple_tests: 

Computes results for small set of six artificial CFGs in cfgs/simple_tests. 

	usage:  ./simple_tests

	output: csv file results/simple_test_results.csv
		stdout


3. apache_small_sample

Computes results for a sample of ~800 apache CFGs in cfgs/apache_cfgs/commons/beanutils-1.9.2/. Running time approximately 5 minues.

	usage:  ./apache_small_sample

	output: csv file results/apache_small_sample_results.csv
		stdout


4. java_small_sample

Computes results for a sample of ~800 java CFGs in cfgs/java_cfgs/alt-rt/. Running time approximately 5 minues.

        usage:  ./java_small_sample

        output: csv file results/apache_small_sample_results.csv
                stdout

5. apache_all (data in paper)

Computes results for all apache CFGs in the data set cfgs/apache_cfgs/. Running time approximately 3 hours.

	usage: ./apache_all

	output: csv file results/apache_all_results.csv
		stdout


6. java_all (data in paper)

Computes results for all apache CFGs in the data set cfgs/java_cfgs. Running t
ime approximately 10 hours.

        usage: ./java_all

        output: csv file results/java_all_results.csv
                stdout



-----------------
scripts/cfgexctractor
-----------------
Contains scripts for extracting control-flow graphs from java bytecodes. You can use that script to generate control-flow graphs for new inputs.  
	
	usage: python main.py -i path/to/a/folder/that/contains/jar/file(s)
	ex   : python main.py -i /home/fse/PathComplexity/lib_jars/apache_commons/bins/commons-cli-1.2/
	
	output: generates .dot files (under outputs/)

Once you have the new control-flow graphs, you can use mathematica script to get path complexity results.
	ex: /usr/local/Wolfram/Mathematica/10.0/Executables/math -script /home/fse/PathComplexity/src/paths.m <path/to/cfgs> Infinity



-----------------
lib_jars
-----------------
Contains Apache commons libraries and Oracle Java 7 runtime libraries. 



-----------------
results
-----------------
Output folder for results from running scripts.

Contains directory 'expected', which has all of the results of running the scripts precomputed.



-----------------
cfgs
-----------------

Control flow graph files in graphviz dot format.

To view a CFG use

$xdot path/to/cfg/file

This control-flow graphs are generated using cfgextractor with the inputs lib_jars/apache_commons lib_jars/jre_lib.

----------------
src
----------------

Contains Mathematica scripts for computing complexities. 

  - paths.m is the main driver. Loads file names, loads and calls modules.
  - pathComplexity.m
  - cyclomaticComplexity.m
  - nPathComplexity.m
  - utils.m
  - cfgextractor_source.jar used to extract CFGs.

  
