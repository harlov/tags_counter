# -*- coding: utf-8 -*-
"""
REST интерфейсы
"""
from flask import request, Blueprint

from tags_counter.exceptions import BadRequest
from .handlers import result
from tags_counter.backend import mongo
from tags_counter.schemas import TAGS_TASK_SCHEMA
from .tasks import calc_tags
from celery.utils import uuid


tags_blueprint = Blueprint('tags', __name__)


@tags_blueprint.route('/', methods=['POST'])
def create_tags_task():
    """
    Добавляет задачу в БД и celery worker
    :return: task
    """
    input_task_obj = TAGS_TASK_SCHEMA.load(request.json)
    if input_task_obj.errors:
        raise BadRequest(input_task_obj.errors)
    input_task = input_task_obj.data
    input_task['task_id'] = uuid()
    mongo.get_db().tasks.insert_one(input_task)

    calc_tags.apply_async(args=(input_task,), task_id=input_task['task_id'])

    return result(TAGS_TASK_SCHEMA.dump(input_task).data)


@tags_blueprint.route('/<string:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Возвращает информацию о задаче, по ее task_id
    :param task_id:
    :return: task
    """
    task = mongo.get_db().tasks.find_one({'task_id': task_id})
    if task is None:
        raise BadRequest('task not found', 404)
    return result(TAGS_TASK_SCHEMA.dump(task).data)

