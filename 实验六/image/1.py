#!/usr/bin/env python
# Designed for use with boofuzz v0.0.9
# coding=utf-8
from boofuzz import *
#���ûỰ��Ϣ�������豸��IP��ַ�Լ��˿�
def main():
    session = Session(
        target=Target(
            connection=SocketConnection("192.168.1.1", 80, proto='tcp')
        ),
    )
#����API�ӿڵ����ݰ�������������boofuzz����ṩ��ԭ���http������ж���
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

        # LINE 3  ��Ӧ Content-Length: 400
        s_static('Content-Length')
        s_static(': ')
        s_size('data', output_format='ascii', fuzzable=True)    
        # size��ֵ����data���ֵĳ����Զ����м��㣬ͬʱ�Ը��ֶν���fuzz
        s_static('\r\n')

        s_static('\r\n')

    # ��Ӧhttp��������
    with s_block('data'):
        s_static('login_name=&curTime=1581845487827&setLang=&setNoAutoLang=&login_n=admin&login_pass=')
        s_string('123456', max_len=1024)
        s_static('&languageSel=1')

    session.connect(s_get("Request"))

    session.fuzz()


if __name__ == "__main__":
    main()