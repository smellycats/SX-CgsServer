#-*- encoding: utf-8 -*-
import ConfigParser


class MyIni:

    def __init__(self, conf_path='my_ini.conf'):
        self.conf_path = conf_path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(conf_path)

    def get_sys(self):
        conf = {}
        section = 'SYS'
        conf['secret_key'] = self.cf.get(section, 'secret_key')
        conf['expires'] = self.cf.getint(section, 'expires')
        conf['white_list_open'] = self.cf.getboolean(section, 'white_list_open')
        conf['white_list'] = self.cf.get(section, 'white_list')
        conf['host'] = self.cf.get(section, 'host')
        conf['port'] = self.cf.getint(section, 'port')
        return conf

    def get_hzhbc(self):
        conf = {}
        section = 'HZHBC'
        conf['db'] = self.cf.get(section, 'db')
        conf['host'] = self.cf.get(section, 'host')
        conf['port'] = self.cf.getint(section, 'port')
        conf['username'] = self.cf.get(section, 'username')
        conf['password'] = self.cf.get(section, 'password')
        return conf

    def get_gdvehicle(self):
        conf = {}
        section = 'GDVEHICLE'
        conf['db'] = self.cf.get(section, 'db')
        conf['host'] = self.cf.get(section, 'host')
        conf['port'] = self.cf.getint(section, 'port')
        conf['username'] = self.cf.get(section, 'username')
        conf['password'] = self.cf.get(section, 'password')
        return conf
