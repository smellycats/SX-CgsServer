# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify

from .. import app, limiter, logger

blueprint = Blueprint('home', __name__)


@blueprint.route('')
@blueprint.route('/')
def index():
    result = {
        'user_url': '%suser{/user_id}' % (request.url_root),
        'scope_url': '%suser/scope' % (request.url_root),
        'token_url': '%stoken' % (request.url_root),
        'gdvehicle_url': '%sgdvehicle{/hphm}{/hpys}' % (request.url_root),
        'hzhbc_url': '%shzhbc{/hphm}{/hpzl}' % (request.url_root)
    }
    return jsonify(result), 200, {'Cache-Control': 'public, max-age=60, s-maxage=60'}



