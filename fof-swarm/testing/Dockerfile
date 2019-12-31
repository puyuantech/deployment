FROM puyuantech/cryptofx:latest
LABEL name="testing"
LABEL maintainer="puyuan<github@puyuan.tech>"

COPY ./resource/* /tmp/resource/

RUN echo -e "\\033[45;37m ############### yum local ############### \033[0m" && \
    yum erase linker -y && \ 
    cd /tmp/resource/ && yum install linker-*-Linux.rpm trader-*-Linux.rpm cryptofx-*-Linux.rpm fof-*-Linux.rpm -y && \
    yum -y clean all && rm -rf /tmp/resource

WORKDIR /shared/
