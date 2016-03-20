# -*- coding: utf-8 -*-
""" Tags counter
    ~~~~~~~~~~~~~~
    REST сервиса подсчета html тегов

"""

from flask import Flask, jsonify
from celery import Celery

from tags_counter.handlers import register_handlers

app = Flask(__name__)
app.config.from_object('config')

celery_app = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)


def register_views():
    from tags_counter.views import tags_blueprint
    app.register_blueprint(tags_blueprint, url_prefix='/tags')

register_handlers(app)
register_views()

