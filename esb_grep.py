#!/usr/bin/python3
import os
import configparser
import argparse
from ssh import Ssh


class esb_grep:

    def __init__(self):
        self.config = self.read_config()
        self.args = self.parse_args()
        cmd = self.make_cmd()
        print(cmd)
        for host in self.config.get('ssh', 'hosts').split(','):
            ssh = Ssh(host, int(self.config.get('ssh', 'port')), self.config.get('ssh', 'login'),
                      self.config.get('ssh', 'password'))
            try:
                grep_out = ssh.remote_cmd(cmd)
                for row in grep_out:
                    print(row)
            except ValueError as e:
                print(e)

    def read_config(self):
        config = configparser.RawConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
        return config

    def parse_args(self):
        arg = argparse.ArgumentParser(description='греп на всех серваках', prog='греп на всех серваках')
        arg.add_argument('-k', type=str, default=None, required=False, help='ключи')
        arg.add_argument('-a', type=bool, default=False, required=False, help='греп по архивным логам')
        arg.add_argument('-s', type=str, default=None, required=True, help='строка по которой ищем')
        arg.add_argument('-f', type=str, default=None, required=True, help='имя файла')
        args = vars(arg.parse_args())
        return args

    def make_cmd(self):
        if self.args['a']:
            cmd = 'zgrep '
            path = '{0}/{1}'.format(self.config.get('ssh', 'old_logs'), self.args['f'])
        else:
            cmd = 'grep '
            path = '/esb/wildfly-8.2.0/standalone/log/{0}'.format(self.args['f'])
        if self.args['k'] is not None:
            keys = self.args['k'].split(',')
            for i in keys:
                cmd += '-{} '.format(i)
        cmd += self.args['s']
        cmd += ' {}'.format(path)
        return cmd

grep = esb_grep()