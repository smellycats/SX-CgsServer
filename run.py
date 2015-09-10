from cgs import app, views
from cgs import debug_logging, online_logging, access_logging

if __name__ == '__main__':
    debug_logging(u'logs/error.log')
    access_logging(u'logs/access.log')
    app.run(host='0.0.0.0', port=8098, threaded=True)
