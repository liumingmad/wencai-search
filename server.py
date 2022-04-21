from http.server import BaseHTTPRequestHandler
from urllib import parse
import cgi
import io
import wencai_search as wc
import json

class WCHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        req_parse = parse.urlparse(self.path)
        message = 'error'
        if req_parse.path == '/wencai/block':
            sn = req_parse.query.split('=')
            message = json.dumps(wc.get_block_data(sn[1]))
        elif req_parse.path == '/wencai/blocklist':
            message = wc.wc_block_list()
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
    

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
