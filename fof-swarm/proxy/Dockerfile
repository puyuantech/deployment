FROM centos:7.2.1511
LABEL name="proxy"
LABEL maintainer="puyuan<github@puyuan.tech>"

EXPOSE 11881
EXPOSE 11882
EXPOSE 11883
EXPOSE 11884
EXPOSE 11885
EXPOSE 11886
EXPOSE 11887
EXPOSE 11888
EXPOSE 11889

COPY ./resource/* /root/

RUN yum install epel-release -y && \
    yum install privoxy -y && \
    yum -y clean all
