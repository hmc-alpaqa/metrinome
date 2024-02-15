FROM ubuntu

RUN apt update
RUN apt install -y git
RUN apt install -y python3
RUN apt install -y pip
RUN apt install -y clang-14
RUN apt install -y llvm-14

# RUN apt install -y clang-6.0 llvm-6.0 llvm-6.0-dev llvm-6.0-tools zsh vim tmux

COPY src/ /app/code/
RUN pip install networkx
RUN pip install pycparser
RUN pip install mpmath
RUN pip install sympy
RUN pip install numpy
RUN pip install networkx
RUN pip install glob2
RUN pip install pandas
RUN pip install wllvm

# RUN pip install clang
RUN CC=/usr/bin/clang

WORKDIR /app/code/
ENV PYTHON_VERSION=3.9.1
ENV PYTHONPATH=/app/code/
CMD ["bash"]