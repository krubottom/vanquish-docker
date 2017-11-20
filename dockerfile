FROM kalilinux/kali-linux-docker
MAINTAINER Karl Rubottom "karl.rubottom@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python python-pip wget python-dev hydra metasploit-framework nmap sqlmap wfuzz \
  exploitdb nikto commix hashcat wordlists cewl git \
  && pip install --upgrade pip \
  && pip install Flask \
  && pip install Flask-wtf \
  && cd /root \
  && git clone https://github.com/frizb/Vanquish \
  && cd /root/Vanquish \
  && python Vanquish2.py -install

ENTRYPOINT /bin/bash
