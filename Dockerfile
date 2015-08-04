FROM selenium/standalone-firefox:latest

ENV DEBIAN_FRONTEND noninteractive

RUN sudo apt-get update -qqy && sudo apt-get install -qqy tightvncserver python-pip
RUN sudo pip install selenium pyvirtualdisplay

ENV WEBSECURIFY_EXTENSION websecurify-5.5.0-fx.xpi

RUN wget -q "https://addons.mozilla.org/firefox/downloads/file/290864/${WEBSECURIFY_EXTENSION}" -O "/tmp/${WEBSECURIFY_EXTENSION}"

ENV VNC_FULL_PASSWORD full
ENV VNC_VIEW_PASSWORD view

RUN mkdir -p ~/.vnc && echo "${VNC_FULL_PASSWORD}\n${VNC_VIEW_PASSWORD}" | vncpasswd -f > ~/.vnc/passwd

RUN sudo mkdir /output

ADD main.py main.py

ENTRYPOINT ["/usr/bin/python", "main.py"]

EXPOSE 5900
VOLUME /output
