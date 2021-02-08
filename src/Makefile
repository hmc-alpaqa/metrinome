SHELL := /bin/bash
UNAME_S := $(shell uname -s)

# ========================
# === Run Inside Image ===
# ========================

lint: fix-lint check-lint

fix-lint:
	isort -l 100 .
	find /app/code -type f -name "*.py" | xargs sed -i -e 's/[[:space:]]*$$//g'
	find /app/code -type f -name "*.py" | xargs sed -i -e 's/	/    /g'

check-lint:
	find /app/code -type f -name "*.py" | xargs pycodestyle --config=./config/pycodestyle # Enforce PEP8.
	find /app/code -type f -name "*.py" | xargs dmypy run -- --config-file=./config/.mypy.ini # Type checking.
	find /app/code -type f -name "*.py" | xargs pydocstyle --count # Enforce docstring formatting.
	find /app/code -type f -name "*.py" | xargs pylint --rcfile=config/pylintrc -r n -f parseable # Linting.

test:
	python -m unittest discover /app/code/tests

coverage:
	coverage run -m unittest discover 
	coverage report -m --omit=tests/*
	coverage xml

clean:
	rm -r __pycache__ || true
	rm -r inlining/__pycache__ || true
	rm -r lang_to_cfg/__pycache__ || true
	rm -r metric/__pycache__ || true
	rm -r tests/__pycache__ || true

# =========================
# === Run Outside Image ===
# =========================

build: 
	docker build --tag harveymudd/metrinome:latest -f ../Dockerfile ../

ifeq ($(UNAME_S),Darwin)
run:
	docker container prune -f --filter "label=metrinome_repl" > /dev/null
	docker run --name metrinome_repl --label metrinome_repl -it -v ${shell pwd}:/app/code harveymudd/metrinome:latest /bin/zsh
else
run:
	docker container prune -f --filter "label=metrinome_repl"
	docker run --name metrinome_repl --label metrinome_repl -it -v ${shell pwd}:/app/code harveymudd/metrinome:latest /bin/zsh
endif


run-detached:
	docker run --name detached_repl -d -it -v $(shell pwd):/app/code harveymudd/metrinome:latest /bin/zsh

start-detached:
	docker start detached_repl

stop-detached:
	docker stop detached_repl -t 10

.PHONY: lint test formatting test build run run-detched stop-detached coverage clean check-lint fix-import stop
	
