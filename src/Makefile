lint:
	mypy main.py # Type checking
	find . -type f -name "*.py" | xargs pylint --rcfile=.pylintrc -r n -f parseable	# Linting
	find . -type f -name "*.py" | xargs pydocstyle # Enforce docstring formatting
	find . -type f -name "*.py" | xargs pycodestyle # Enforce PEP8

lint_score_only:
	mypy main.py # Type checking
	find . -type f -name "*.py" | xargs pylint --rcfile=.pylintrc -r n -f parseable | grep "code"

tests:
	python tests/test_command.py
	python tests/test_cpp.py
	python tests/test_cyclomatic.py
	python tests/test_graph.py
	python tests/test_java.py
	python tests/test_log.py
	python tests/test_metrics.py
	python tests/test_npath.py
	python tests/test_pathcomplexity.py
	python tests/test_python.py
	python tests/test_utils.py

test:   formatting lint tests

build: 
	# pass 

run:
	# pass

# Tested on MacOS (will likely not work on linux due to slight differences in 
# the 'sed' command.
formatting:
	# Remove trailing whitespace
	find . -type f -name "*.py" | xargs sed -i '' -e "s/[[:space:]]*$$//g"
	# Replace tabs with spaces 
	find . -type f -name "*.py" | xargs sed -i '' -e "s/	/    /g"

clean:
	# nothing

.PHONY: lint tests clean formatting test build run
	
