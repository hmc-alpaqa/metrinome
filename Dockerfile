FROM python:3.9-slim 
WORKDIR /app
COPY requirements.txt /app/ 
COPY ./examples /app/examples/
RUN pip install --trusted-host pypi.python.org -r requirements.txt 
RUN mkdir -p /usr/share/man/man1 && apt-get update && apt-get install -y build-essential wget software-properties-common openjdk-11-jdk-headless
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - 
RUN apt-get update

# Get KLEE dependencies (LLVM 6.0) [http://klee.github.io/build-llvm60/]
RUN apt-get install -y curl libcap-dev git unzip doxygen libsqlite3-dev libgoogle-perftools-dev libtcmalloc-minimal4 cmake libncurses5-dev
RUN pip install tabulate
RUN apt-get install -y clang-6.0 llvm-6.0 llvm-6.0-dev llvm-6.0-tools zsh vim tmux
RUN apt-get install -y g++-multilib
# Install z3 
RUN git clone https://github.com/Z3Prover/z3/ 
RUN cd /app/z3 && git pull && git reset --hard 2d1684bc2d2621c0d6b02b81168624388648049a 
RUN cd /app/z3 && python scripts/mk_make.py 
RUN cd /app/z3/build && make && make install
RUN pip install z3-solver

# Install lit
RUN pip install lit

# Build uClibc and the POSIX environment model 
RUN git clone https://github.com/klee/klee-uclibc.git
RUN ln -s /usr/bin/llvm-config-6.0 /usr/bin/llvm-config
RUN alias llvm-config=llvm-config-6.0 
RUN CC=/usr/bin/clang-6.0 /app/klee-uclibc/configure --make-llvm-lib
RUN cd /app/klee-uclibc && make -j2

# Get KLEE
RUN mkdir /app/build
RUN git clone https://github.com/klee/klee.git
RUN apt-get install zlib1g-dev
RUN cd /app/build && cmake -DENABLE_SOLVER_STP=OFF -DENABLE_POSIX_RUNTIME=ON -DENABLE_KLEE_UCLIBC=ON -DKLEE_UCLIBC_PATH=/app/klee-uclibc -DENABLE_UNIT_TESTS=OFF -DLLVMCC=/usr/bin/clang-6.0 -ENABLE_ZLIB=OFF -DLLVMCXX=/usr/bin/clang++-6.0 /app/klee
RUN cd /app/build && make

# Build LibC++
RUN pip install wllvm
# TODO:
# RUN LLVM_VERSION=6.0 SANITIZER_BUILD= BASE=/app/libcxx /app/klee/scripts/build/build.sh libcxx

# Get Google test sources
RUN curl -OL https://github.com/google/googletest/archive/release-1.7.0.zip
RUN unzip /app/release-1.7.0.zip

# C Parser written in python 
RUN pip install pycparser
RUN git clone https://github.com/eliben/pycparser

ENV PATH "$PATH:/app/build/bin/"

# AFL (Dependency for Kelinci) 
RUN git clone https://github.com/google/AFL

# Kelinci: https://github.com/isstac/kelinci
RUN git clone https://github.com/isstac/kelinci

# JQF + Zest 
RUN git clone https://github.com/rohanpadhye/jqf

# JPF (Symbolic Java Path Finder): https://github.com/SymbolicPathFinder/jpf-symbc 
# Refer to https://github.com/SymbolicPathFinder/jpf-symbc/wiki/Documentation 
RUN git clone https://github.com/javapathfinder/jpf-core
RUN git clone https://github.com/SymbolicPathFinder/jpf-symbc
RUN mkdir jpf && mv jpf-core jpf && mv jpf-symbc jpf 
COPY site.properties /app/jpf/

# PRISM: https://www.prismmodelchecker.org/manual/InstallingPRISM/Instructions#binaries 
COPY /dependencies/prism-4.5-linux64.tar.gz /app/
RUN gunzip prism-4.5-linux64.tar.gz && tar xf prism-4.5-linux64.tar && cd prism-4.5-linux64 && ./install.sh

# Clean up the files
RUN rm -rf /app/prism-4.5-linux64.tar && rm /app/requirements.txt && rm /app/release-1.7.0.zip

# Set up oh-my-zsh [OPTIONAL]
RUN echo "y" | sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

RUN mkdir /app/code/
ENV PYTHONPATH "/app/code/"
WORKDIR /app/code/
