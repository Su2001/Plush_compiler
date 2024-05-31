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
COPY codegen/ /plush/codegen/
COPY requirements.txt /plush/requirements.txt
COPY debug/ /plush/debug/
COPY parsetab.py /plush/parsetab.py
COPY plush_testsuite/ /plush/plush_testsuite/
COPY utils/ /plush/utils/
COPY tokens.py /plush/tokens.py
COPY main.py /plush/main.py
COPY parseRules.py /plush/parseRules.py
COPY semantic.py /plush/semantic.py
COPY plush.sh /plush/plush.sh
COPY plush.sh /plush/execute.sh



WORKDIR /plush
RUN pip3 install -r requirements.txt

RUN chmod +x plush.sh

