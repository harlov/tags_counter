# -*- coding: utf-8 -*-
"""
Обертки для REST-ответов.
"""
from flask import jsonify

from tags_counter.exceptions import BadRequest


def result(res_obj):
    return jsonify({'result': res_obj}), 200


def register_handlers(app):
    @app.errorhandler(BadRequest)
    def bad_request_handler(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
