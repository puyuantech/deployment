FROM centos:7.2.1511
LABEL name="proxy"
LABEL maintainer="puyuan<github@puyuan.tech>"

EXPOSE 1187

COPY ./resource/privoxy.config /root/privoxy.config

RUN yum install epel-release -y && \
    yum install privoxy -y && \
    yum -y clean all

CMD /bin/bash -c "privoxy --no-daemon /root/privoxy.config"