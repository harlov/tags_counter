# -*- coding: utf-8 -*-
"""
Задача просчета тегов для celery
"""
import re
from collections import Counter

import requests
from tags_counter import celery_app
from tags_counter.backend import mongo
from tags_counter.schemas import TagsTaskSchema

# pylint: disable=C0103
find_tags_re = re.compile(r'<([\w\d-]+)')
# pylint: enable=C0103


def extract_tags(text):
    """
    Считает все открывающие html теги
    :param text: html текст
    :return: словарь, в формате тег:количество
    """
    find_res = find_tags_re.findall(text)
    return Counter(find_res)


@celery_app.task()
def calc_tags(input_task):
    """
    Получает страницу по URL, считает html теги, и сохраняет результат или ошибку в базу
    :param input_task:
    :return:
    """
    mongo.get_db().tasks.update_one({'task_id': input_task['task_id']}, {'$set': {
        'state': TagsTaskSchema.STATE_RUN
    }})

    response = requests.get(input_task['target_url'])
    if response.status_code != 200:
        mongo.get_db().tasks.update_one({'task_id': input_task['task_id']}, {'$set': {
            'state': TagsTaskSchema.STATE_ERROR,
            'result': response.status_code
        }})

    count_res = extract_tags(response.text)

    mongo.get_db().tasks.update_one({'task_id': input_task['task_id']}, {'$set': {
        'result': count_res,
        'state': TagsTaskSchema.STATE_DONE
    }})
