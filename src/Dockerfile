FROM ubuntu

RUN apt update
RUN apt install -y git
RUN apt install -y wget
RUN apt install -y python3
RUN apt install -y python3.12-venv
RUN apt install -y pip
RUN apt install -y clang-14
RUN apt install -y llvm-14
RUN apt install -y curl
RUN apt install -y unzip
# RUN apt install -y openjdk-19-jdk openjdk-19-jre

#[WARNING] could be sketchy oops
RUN wget https://download.oracle.com/java/19/archive/jdk-19.0.2_linux-x64_bin.deb
RUN apt -qqy install ./jdk-19.0.2_linux-x64_bin.deb
RUN update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-19/bin/java 1919


# RUN apt install -y clang-6.0 llvm-6.0 llvm-6.0-dev llvm-6.0-tools zsh vim tmux

# COPY src/ /app/code/
RUN python3 -m venv ./myvenv
# RUN rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED
RUN . ./myvenv/bin/activate && pip install networkx pycparser mpmath sympy numpy glob2 pandas wllvm cpgqls-client virtualenv
RUN . ../../myvenv/bin/activate

RUN curl -L https://github.com/ShiftLeftSecurity/joern/releases/latest/download/joern-install.sh | bash

# RUN pip install clang
RUN CC=/usr/bin/clang


WORKDIR /app/code/



ENV PYTHON_VERSION=3.9.1
ENV PYTHONPATH=/app/code/
# RUN chmod u+x Benchmark.sh

ENV PATH = "${PATH}:/opt/joern/joern-cli"
ENV PATH="/myvenv/bin:${PATH}"

# customize command line prompt to look nice :)
RUN /bin/bash -c "echo \"PS1='\[\033[01;32m\]➜ \[\033[00m\] \[\033[01;36m\]\W \[\033[00m\]'\" >> /root/.bashrc "

# CMD ["bash","../../opt/joern/joern-cli/joern --server"]