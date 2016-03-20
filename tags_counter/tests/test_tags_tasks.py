# -*- coding: utf-8 -*-

from unittest import TestCase
import requests_mock

from tags_counter import celery_app
from tags_counter.backend import mongo
from tags_counter.tasks import calc_tags


class TestTagsTasks(TestCase):
    """
    Должен выполнить задачу, изменить ее статус на "done"
    """

    def setUp(self):
        mongo.get_connection().drop_database('test')
        celery_app.conf.update({'MONGODB_NAME': 'test'})

    def test_run_normal_url(self):
        celery_app.conf.update({'CELERY_ALWAYS_EAGER': True})
        mock_input = {'target_url': 'http://testpage.test', 'task_id': 'la-la-la'}

        with requests_mock.Mocker() as m:
            with open('./test_set_openflashcards.html') as test_set_content:
                m.get('http://testpage.test', text=test_set_content.readline(), headers={'Content-Type': 'text/html'})
            mongo.get_db().tasks.insert_one(mock_input)
            response = calc_tags.apply_async(args=(mock_input,), task_id=mock_input['task_id'])
            task_instance = mongo.get_db().tasks.find_one({'task_id': mock_input['task_id']})

            self.assertEqual(task_instance['state'], 'done')
            self.assertIsNotNone(task_instance['result'])