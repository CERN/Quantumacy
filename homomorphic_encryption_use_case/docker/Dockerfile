# ----------------------------------------------------------------------------
# Created By  : José Cabrero-Holgueras
# Created Date: 01/2022
# Copyright: CERN
# License: MIT
# version ='1.0'
# ---------------------------------------------------------------------------

FROM ubuntu:latest

ARG USER=none
ARG GROUP=none
ARG UID=none
ARG GID=none
ARG PW=docker
ARG ENV_NAME=anacondo

RUN groupadd -g ${GID} ${GROUP}
RUN useradd -s /bin/bash -d /home/${USER} --uid=${UID} -m -G sudo ${USER} && echo "${USER}:${PW}" | chpasswd

# Base image is Ubuntu and needed tools for Linux usage
# Getting python and related tools
# Getting net-tools and ping
# Getting zlib - Compression of HE
RUN ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime

RUN apt-get update -y && apt-get upgrade -y && \
apt-get install -y build-essential  software-properties-common bash-completion man  manpages-posix && \ 
apt-get install -y python3 python3-pip virtualenv python3-numpy python3-dev python3-wheel && \
apt-get install -y vim git wget curl unzip sudo && \
apt-get install -y net-tools iputils-ping dnsutils


# Creating the .bashrc files
RUN echo "PS1='\[\033[01;31m\](docker) \[\e[01;36m\]\u\[\e[01;37m\]@\[\e[01;33m\]\H\[\e[01;37m\]:\[\e[01;32m\]\w\[\e[01;37m\]\$\[\033[0;37m\] '" >> /root/.bashrc && \
echo "alias python=python3" >> /root/.bashrc && \
echo "alias pip=pip3" >> /root/.bashrc

# Creating the .bashrc files
RUN echo "PS1='\[\033[01;31m\](docker) \[\e[01;36m\]\u\[\e[01;37m\]@\[\e[01;33m\]\H\[\e[01;37m\]:\[\e[01;32m\]\w\[\e[01;37m\]\$\[\033[0;37m\] '" >> /home/${USER}/.bashrc && \
echo "alias python=python3" >> /home/${USER}/.bashrc && \
echo "alias pip=pip3" >> /home/${USER}/.bashrc

# Install CMAKE to /root/deps/cmake
RUN mkdir -p /usr/local/go/bin && cd /root/ && \
wget https://go.dev/dl/go1.17.6.linux-amd64.tar.gz && \
tar -xf go1.17.6.linux-amd64.tar.gz -C /usr/local/ && \
rm go1.17.6.linux-amd64.tar.gz

# Adding go to the path
ENV PATH /usr/local/go/bin:$PATH

# Creating the user and id
USER ${USER}:${GID}
WORKDIR /home/${USER}

# Downloading Anaconda
RUN wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh && \
bash Anaconda3-2021.11-Linux-x86_64.sh -b && \
rm Anaconda3-2021.11-Linux-x86_64.sh

# Adding Anaconda to the path
ENV PATH /home/${USER}/anaconda3/bin:$PATH


# Updating Anaconda
RUN conda update conda && \
conda update anaconda && \
conda update --all

# Creating a new environment
RUN conda create -n ${ENV_NAME} anaconda

# Creating new environment
RUN conda install -n ${ENV_NAME} -c anaconda flask

RUN conda init 

RUN echo "source activate ${ENV_NAME}" >> /home/${USER}/.bashrc

RUN bash -c "/home/${USER}/anaconda3/envs/${ENV_NAME}/bin/pip3 install QKDSimkit"

CMD ["bash"]
