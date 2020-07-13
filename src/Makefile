lint:
	find . -type f -name "*.py" | xargs pycodestyle --config=./config/pycodestyle # Enforce PEP8.
	find . -type f -name "*.py" | xargs mypy # Type checking.
	find . -type f -name "*.py" | xargs pydocstyle --count # Enforce docstring formatting.
	find . -type f -name "*.py" | xargs pylint --rcfile=.pylintrc -r n -f parseable	# Linting.

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

coverage:
	coverage run -m unittest discover 
	coverage report -m --omit=tests/*

test:   formatting lint tests

build: 
	docker build --tag harveymudd/metrinome:latest -f ../Dockerfile ../

run:
	docker run -it -v ${shell pwd}:/app/code harveymudd/metrinome:latest /bin/zsh

run-detached:
	docker run --name detached_repl -d -t -v $(shell pwd):/app/code harveymudd/metrinome:latest

stop-detached:
	docker stop detached_repl -t 10

# Tested on MacOS (will likely not work on linux due to slight differences in the 'sed' command.
formatting:
	# Remove trailing whitespace.
	find . -type f -name "*.py" | xargs sed -i '' -e "s/[[:space:]]*$$//g"
	# Replace tabs with spaces.
	find . -type f -name "*.py" | xargs sed -i '' -e "s/	/    /g"
	# Replace ''' with """.
	find . -type f -name "*.py" | xargs sed -i '' -e 's/'"'''"'/"""/g'

.PHONY: lint tests formatting test build run run-detched stop-detached coverage
	
