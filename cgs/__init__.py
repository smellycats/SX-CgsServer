import logging

from flask import Flask
from flask_limiter import Limiter, HEADERS
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

from config import Production
from my_logger import debug_logging, online_logging, access_logging


app = Flask(__name__)
app.config.from_object(Production())

db = SQLAlchemy(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

debug_logging(u'logs/error.log')
access_logging(u'logs/access.log')

logger = logging.getLogger('root')
access_logger = logging.getLogger('access')

limiter = Limiter(app, headers_enabled=True, global_limits=["10/minute"])
limiter.header_mapping = {
    HEADERS.LIMIT: "X-RateLimit-Limit",
    HEADERS.RESET: "X-RateLimit-Reset",
    HEADERS.REMAINING: "X-RateLimit-Remaining"
}

from .views import home, token, user, gd_vehicle, hz_hbc

app.register_blueprint(home.blueprint, url_prefix='/')
app.register_blueprint(token.blueprint, url_prefix='/token')
app.register_blueprint(user.blueprint, url_prefix='/user')
app.register_blueprint(gd_vehicle.blueprint, url_prefix='/gdvehicle')
app.register_blueprint(hz_hbc.blueprint, url_prefix='/hzhbc')

##app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../cgs.db'
##app.config['SQLALCHEMY_BINDS'] = {
##    'cgs': 'mysql://root:root@127.0.0.1/cgs',
##    'hbc': 'mysql://root:root@127.0.0.1/hbc'
##}
