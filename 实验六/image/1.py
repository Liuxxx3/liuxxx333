#!/usr/bin/env python
# Designed for use with boofuzz v0.0.9
# coding=utf-8
from boofuzz import *
#设置会话信息，包括设备的IP地址以及端口
def main():
    session = Session(
        target=Target(
            connection=SocketConnection("192.168.1.1", 80, proto='tcp')
        ),
    )
#根据API接口的数据包构造请求，利用boofuzz框架提供的原语对http请求进行定义
    s_initialize(name="Request")
    with s_block("Request-Line"):
        # LINE 1
        s_static("POST", name="Method")
        s_delim(" ", name='space-1')
        s_string("/fromLogin", name='Request-URI')  # variation
        s_delim(" ", name='space-2')
        s_static('HTTP/1.1', name='HTTP-Version')   
        s_static("\r\n")

        # LINE 2
        s_static("Host", name="Host")
        s_static(": ")
        s_static("192.168.1.1", name="ip")
        s_static("\r\n")

        # LINE 3  对应 Content-Length: 400
        s_static('Content-Length')
        s_static(': ')
        s_size('data', output_format='ascii', fuzzable=True)    
        # size的值根据data部分的长度自动进行计算，同时对该字段进行fuzz
        s_static('\r\n')

        s_static('\r\n')

    # 对应http请求数据
    with s_block('data'):
        s_static('login_name=&curTime=1581845487827&setLang=&setNoAutoLang=&login_n=admin&login_pass=')
        s_string('123456', max_len=1024)
        s_static('&languageSel=1')

    session.connect(s_get("Request"))

    session.fuzz()


if __name__ == "__main__":
    main()