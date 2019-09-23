FROM python:3.7-slim 
# Uses debian:buster-slim 
WORKDIR /app
COPY ./src /app 
COPY requirements.txt /app
COPY ./examples /app  
RUN pip install --trusted-host pypi.python.org -v -r requirements.txt 
RUN apt-get update && apt-get install -y build-essential wget software-properties-common
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-6.0 main"
RUN apt-get update && apt-get insatll -y clang-6.0 llvm 