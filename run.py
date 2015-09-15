from cgs import app, views
from cgs import debug_logging, online_logging, access_logging
from ini_conf import MyIni

if __name__ == '__main__':
    debug_logging(u'logs/error.log')
    access_logging(u'logs/access.log')
    my_ini = MyIni('my_ini.conf')
    s_ini = my_ini.get_sys()
    h_ini = my_ini.get_hzhbc()
    v_ini = my_ini.get_gdvehicle()
    app.config['SECRET_KEY'] = s_ini['secret_key']
    app.config['EXPIRES'] = s_ini['expires']
    app.config['WHITE_LIST_OPEN'] = s_ini['white_list_open']
    app.config['WHITE_LIST'] = set(s_ini['white_list'].split(','))
    app.config['SQLALCHEMY_BINDS'] = {
        'cgs': 'mysql://%s:%s@%s:%s/%s' % (v_ini['username'], v_ini['password'],
                                           v_ini['host'], v_ini['port'],
                                           v_ini['db']),
        'hbc': 'mysql://%s:%s@%s:%s/%s' % (h_ini['username'], h_ini['password'],
                                           h_ini['host'], h_ini['port'],
                                           h_ini['db'])
    }

    app.run(host='0.0.0.0', port=8098, threaded=True)
