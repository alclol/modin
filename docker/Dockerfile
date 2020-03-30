FROM continuumio/miniconda3

RUN conda install -c conda-forge psutil setproctitle
RUN apt upgrade
RUN apt install libhdf5-dev
RUN pip install modin
