# -*- coding: UTF-8 -*-

from http.server import BaseHTTPRequestHandler
from urllib import parse
import cgi
import io
import wencai_search as wc
import json
import os

class WCHandler(BaseHTTPRequestHandler):
    def is_res(self, path):
        sub = path[path.rfind('.')+1:len(path)]
        return sub in ['html', 'js', 'css']

    def get_content_type(self, path):
        content_type = 'text/html; charset=utf-8'  
        sub = path[path.rfind('.')+1:len(path)]
        if sub == 'html':
            content_type = 'text/html; charset=utf-8' 
        elif sub == 'js':
            content_type = 'text/javascript; charset=utf-8' 
        elif sub == 'css':
            content_type = 'text/css; charset=utf-8' 
        return content_type

    def send_wc_response(self, code, message, content_type):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))


    def do_GET_res(self, path):
        path = path[1:len(path)]
        if not os.path.exists(path):
            self.send_wc_response(404, '404 error', self.get_content_type(path))
            return
        with open(path, 'r') as f:
            self.send_wc_response(200, f.read(), self.get_content_type(path))

    def check_token(self, token):
        # import hmac
        # import config
        # key = config.wc_util_password.encode("utf-8")
        # raw = 'Helloworld!'.encode("utf-8")
        # hashed = hmac.new(key, raw, 'sha1').hexdigest()
        return token == 'cb01b64fce16b2092e30a593879c8bd192184a05'


    def do_GET(self):
        req_parse = parse.urlparse(self.path)

        if self.is_res(req_parse.path):
            self.do_GET_res(req_parse.path)
            return

        if not self.check_token(self.headers.get('token')):
            print('token error')
            self.send_wc_response(400, 'token error', 'text/html; charset=utf-8') 
            return
        
        if req_parse.path == '/wencai/block':
            sn = req_parse.query.split('=')
            message = wc.get_block_data(sn[1]).to_html(classes='stock-table')
            self.send_wc_response(200, message, 'text/html; charset=utf-8') 
            return

        if req_parse.path == '/wencai/blocklist':
            message = wc.wc_block_list()
            self.send_wc_response(200, message, 'application/json; charset=utf-8') 
            return


    def do_POST(self):
        # 分析提交的表单数据
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # 开始回复
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )

        out.write('Client: {}\n'.format(self.client_address))
        out.write('User-agent: {}\n'.format(
            self.headers['user-agent']))
        out.write('Path: {}\n'.format(self.path))
        out.write('Form data:\n')

        # 表单信息内容回放
        for field in form.keys():
            out.write('\t{}={}\n'.format(field, form[field].value))

        # 将编码 wrapper 到底层缓冲的连接断开， 
        # 使得将 wrapper 删除时， 
        # 并不关闭仍被服务器使用 socket 。
        out.detach()


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), WCHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
