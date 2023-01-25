# syntax=docker/dockerfile:1

FROM continuumio/miniconda3:latest

WORKDIR /sybil-app

COPY requirements.txt requirements.txt
RUN conda install --yes --file requirements.txt
RUN pip3 install --upgrade pip
RUN pip install eth-abi

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]