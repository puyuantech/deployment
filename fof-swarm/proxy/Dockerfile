FROM centos:7.2.1511
LABEL name="proxy"
LABEL maintainer="puyuan<github@puyuan.tech>"

EXPOSE 1187

COPY ./resource/* /root/

RUN yum install epel-release -y && \
    yum install privoxy -y && \
    yum -y clean all && rm -rf /tmp/resource

CMD /bin/bash -c "privoxy --no-daemon /root/privoxy.config"