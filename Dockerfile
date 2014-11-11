FROM ubuntu:14.04

MAINTAINER Richard Crook richard@pinkgrass.org

# make sure the package repository is up to date
RUN apt-get update

# install openssh server
RUN apt-get -y install openssh-server; mkdir -p /var/run/sshd; locale-gen en_US en_US.UTF-8

# install supervisord
#RUN apt-get -y install supervisor
#ADD supervisord.conf /etc/supervisor/supervisord.conf
#RUN mkdir -p /var/log/supervisor

# install python3 and pip for python3
RUN apt-get install -y python3-pip

# set root password
RUN echo 'root:rootpasswd' | chpasswd

# motd
#RUN rm -rf /etc/update-motd.d /etc/motd
#ADD motd /etc/motd



EXPOSE 8888 22

# run container with supervisor
CMD ["/usr/bin/python3 "]

