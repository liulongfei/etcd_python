#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 16/11/1 15:49


from __future__ import unicode_literals
import sys
import os
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import quote, unquote

from argparse import ArgumentParser
from etcd.client import Client


class ToolsEtcd(object):
    def __init__(self, host, port=2379):
        self.host = host
        self.port = port

    @property
    def _conn_etcd(self):
        """ 连接服务器 """
        # 解析ip
        if ',' and ':' in self.host:
            host = []
            for k, v in (u.split(':') for u in (i for i in self.host.split(','))):
                host.append((k, int(v)))
            host = tuple(host)
        elif ':' in self.host:
            host = tuple(self.host.split(':'))
        else:
            host = self.host

        client = Client(host=host, port=self.port, allow_reconnect=True)
        return client

    def put_data(self, key, value):
        """ 上传数据 """
        client = self._conn_etcd

        try:
            client.write(key=key, value=value)

            return {'code': 200, 'message': 'set success.', 'key': key}
        except Exception as e:
            return {'code': 500, 'message': e}

    def get_data(self, key):
        """ 获取数据 """
        try:
            client = self._conn_etcd

            return client.read(key).value
        except Exception as e:
            return {'code': 500, 'message': e}


def arg():
    parser = ArgumentParser(usage='%(prog)s --host HOST --port PORT --key KEY --value VALUE')

    # 主机
    hosts_default = os.environ.get('PYTHON_ETCD_HOSTS') if os.environ.get('PYTHON_ETCD_HOSTS') else '127.0.0.1:2379'
    parser.add_argument('-H', '--hosts', default=hosts_default, action='store', type=str,
                        dest='hosts', help='etcd server ip address.')

    # 端口
    port_default = int(os.environ.get('PYTHON_ETCD_PORT')) if os.environ.get('PYTHON_ETCD_PORT') else 2379
    parser.add_argument('-p', '--port', default=port_default, type=int, action='store',
                        dest='port', help='etcd listen port.')

    # key
    key_default = os.environ.get('PYTHON_ETCD_KEY') if os.environ.get('PYTHON_ETCD_KEY') else ''
    parser.add_argument('-k', '--key', default=key_default, action='store', type=str,
                        dest='key', help='etcd key name.')

    # value , 当数据需要转码的时候,此参数为文件名字
    value_default = os.environ.get('PYTHON_ETCD_VALUE') if os.environ.get('PYTHON_ETCD_VALUE') else ''
    parser.add_argument('-v', '--value', default=value_default, action='store', type=str,
                        dest='value', help='etcd key value.')

    # type
    type_default = os.environ.get('PYTHON_ETCD_TYPE') if os.environ.get('PYTHON_ETCD_TYPE') else 'get'
    parser.add_argument('-t', '--type', default=type_default, action='store', type=str,
                        dest='type', help='Operating etcd Type, put or get.')

    # 数据是否转码为url
    parser.add_argument('-e', '--encode', default=False, action="store_true", dest='encode',
                        help='etcd value url encode data.')

    # url 码转为 str
    parser.add_argument('-d', '--decode', default=False, action="store_true", dest='decode',
                        help='etcd value url decode data.')

    return parser.parse_args()


def main():
    options = vars(arg())
    client = ToolsEtcd(host=options.get('hosts'), port=options.get('port'))

    if options.get('encode') and options.get('type') == 'put':
        # 上传文件数据
        with open(options.get('value'), 'r') as f:
            # url encode
            data = quote(f.read())

        message = client.put_data(key=options.get('key'), value=data)
        return message

    elif options.get('type') == 'put':
        # 上传普通数据
        message = client.put_data(key=options.get('key'), value=options.get('value'))
        return message

    elif options.get('decode') and options.get('type') == 'get' and options.get('value'):
        # 获取文件数据 并转码写入文件
        message = client.get_data(key=options.get('key'))
        if sys.version_info < (3, 0):
            # etcd get 得到的 unicode, 转化为str
            message = message.encode('ascii')

        with open(options.get('value'), 'w') as f:
            # unquote 只能处理 str 类型
            f.write(unquote(message))

        return message
    elif options.get('decode') and options.get('type') == 'get':
        # 获取数据 并转码
        message = client.get_data(key=options.get('key'))
        # etcd get 得到的 unicode, 转化为str
        message_str = message.encode('ascii')

        return message_str
    elif options.get('type') == 'get' and options.get('value'):
        # 获取数据 写入文件
        message = client.get_data(key=options.get('key'))

        with open(options.get('value'), 'w') as f:
            # unquote 只能处理 str 类型
            f.write(message)
        return message

    elif options.get('type') == 'get':
        # 获取普通数据
        message = client.get_data(key=options.get('key'))
        return message

if __name__ == '__main__':
    print(main())
