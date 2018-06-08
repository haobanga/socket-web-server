import time
import os
from jinja2 import Environment, FileSystemLoader

# __file__ 就是本文件的名字
# 得到用于加载模板的目录
path = '{}/templates/'.format(os.path.dirname(__file__))
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


def template_render(path,**kwargs):
    # 模板渲染
    template = env.get_template(path)
    return template.render(**kwargs)

    
def response_with_headers(headers, status_code=200):
    http_headers = {
        'Content-Type': 'text/html',
    }
    if not headers is None:
        http_headers.update(headers)
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in http_headers.items()])
    return header
    
    
def redirect(location, headers=None):
    h = {}
    if headers is not None:
        h.update(headers)
    h['Location'] = location
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')

   
def http_response(body, headers=None,status_code=200):
    """
    headers 是可选的字典格式的 HTTP 头
    """
    header = response_with_headers(headers, status_code)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')    
