#from requests_func import RequestsFunc
from ini_conf import MyIni
from cgs import db
from cgs import Users


def ini_test():
    myini = MyIni()
    try:
        print myini.get_kakou()
        print myini.get_hbc()
        print myini.get_mysql()
        print myini.get_syst()
    except ConfigParser.NoOptionError as e:
        print e

def model_test():
    #db.connect()

    Users.create_table()
    #db.close()

if __name__ == '__main__':
    #model_test()
    #conf_test()
    #log_test()
    model_test()
    #flask_run_test()
