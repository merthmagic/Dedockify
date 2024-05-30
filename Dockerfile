FROM alpine:3.11.3

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk --no-cache update && apk add --no-cache python3 wget \
    && wget -q --no-check-certificate https://bootstrap.pypa.io/get-pip.py \
    && apk del wget && python3 get-pip.py && rm -f get-pip.py \
    && pip install -U docker pip -i https://pypi.tuna.tsinghua.edu.cn/simple && yes | pip uninstall pip

RUN mkdir /app
COPY entrypoint.sh /.
COPY dedockify.py /app/.

ENTRYPOINT ["/entrypoint.sh"]
