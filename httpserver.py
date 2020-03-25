# -*- coding: utf-8 -*-

import sys
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
#大家直接在浏览器中输入链接，浏览器拿到地址以后，默认是采用GET方式向服务器发送请求。
#从服务器获取数据，使用get方面，向服务器提交数据，使用post方法。
#在 python 的 BaseHTTPRequestHandler 类中 ，do_XXX函数，就是处理对应的客户端请求的函数。
#所以指定了 MyHTTPRequestHandler 来处理 http请求，那么当用get方法请求，就会调用 do_GET,POST方法请求，就会调用 do_POST函数
#

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    field_name = 'a'
    form_html = \
        '''
        <html>
        <body>
        <form method='post' enctype='multipart/form-data'>
        <input type='text' name='%s'>
        <input type='submit'>
        </form>
        </body>
        </html>
        ''' % field_name
    #表单以变量名变量值的方式组织，input的name相当于变量名，你填入的数据就是变量值。
    #python的cgi.FieldStorage将form组织为python的dict数据类型
    #所以可以通过  form_data['field_name'].value 获得所填入的数据
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        try:
            file = open("."+self.path, "rb")
        except FileNotFoundError as e:#文件不存在则新建
            print(e)
            self.wfile.write(self.form_html.encode())
        else:#文件存在则直接把文件内容写给浏览器
            content = file.read()
            self.wfile.write(content)

    def do_POST(self):#在表单中填入数据。点提交按钮。然后服务器的do_POST函数会被调用。
        #这里通过 cgi.FieldStorage解析了客户端提交的请求，
        #原始的请求的头部在self.headers。body部分在self.rfile
        #解析完成以后放到 form_data变量里，其中form_data['field_name'].value,就是在编辑框中填入的数据。
        form_data = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            })
        fields = form_data.keys()
        if self.field_name in fields:
            input_data = form_data[self.field_name].value
            file = open("."+self.path, "wb")
            file.write(input_data.encode())

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body>OK</body></html>")


class MyHTTPServer(HTTPServer):
    def __init__(self, host, port):
        print("run app server by python!")
        HTTPServer.__init__(self,  (host, port), MyHTTPRequestHandler)


if '__main__' == __name__:
    server_ip = "0.0.0.0"
    server_port = 8080
    if len(sys.argv) == 2:
        server_port = int(sys.argv[1])
    if len(sys.argv) == 3:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
    print("App server is running on http://%s:%s " % (server_ip, server_port))

    server = MyHTTPServer(server_ip, server_port)
    server.serve_forever()
#通常，一个静态的http服务器，这里的路径就是http服务器根目录下的文件，动态服务器这里可能是文件和参数，或者是对应其他服务器后台的处理过程。
#例如 http://127.0.0.1:8080/a.php?p1=x 指定有a.php来处理这个请求，参数是p1=x 问号后面是参数，可以有多个
