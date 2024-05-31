FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y\
    python3 \
    python3-pip\
    llvm \
    clang \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /plush
COPY src/ /plush/src/
COPY requirements.txt /plush/requirements.txt
COPY plush_testsuite/ /plush/plush_testsuite/
COPY aux_functions.c /plush/aux_functions.c
COPY plush.sh /plush/plush.sh
COPY execute.sh /plush/execute.sh



WORKDIR /plush
RUN pip3 install -r requirements.txt

RUN chmod +x plush.sh
RUN chmod +x execute.sh

