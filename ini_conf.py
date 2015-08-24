#-*- encoding: utf-8 -*-
import ConfigParser

class MyIni:
    def __init__(self, confpath = 'my_ini.conf'):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(confpath)
    
    def get_kakou(self):
        conf = {}
        conf['host']     = self.cf.get('KAKOU', 'host')
        conf['port']     = self.cf.getint('KAKOU', 'port')
        conf['user']     = self.cf.get('KAKOU', 'user')
        conf['password'] = self.cf.get('KAKOU', 'password')
        return conf
    
    def get_hbc(self):
        conf = {}
        conf['host']     = self.cf.get('HBC', 'host')
        conf['port']     = self.cf.getint('HBC', 'port')
        conf['user']     = self.cf.get('HBC', 'user')
        conf['password'] = self.cf.get('HBC', 'password')
        return conf

    def get_mysql(self):
        conf = {}
        conf['host']     = self.cf.get('MYSQLSET','host')
        conf['port']     = self.cf.getint('MYSQLSET','port')
        conf['user']     = self.cf.get('MYSQLSET','user')
        conf['password'] = self.cf.get('MYSQLSET','password')
        conf['db']       = self.cf.get('MYSQLSET','db')
        return conf

    def get_syst(self):
        conf = {}
        conf['id_flag'] = self.cf.getint('SYSTSET','id_flag')
        conf['imgpath'] = self.cf.get('SYSTSET','imgpath')
        return conf

 
if __name__ == "__main__":
    try:
        hbcini = Hbc_ini()
        print hbcini.getHzkk()
        #s = imgIni.getPlateInfo(PATH2)

    except ConfigParser.NoOptionError,e:
        print e
        time.sleep(10)

