
# -*- coding: utf-8 -*-
import json
import unittest

import mongomock
from mock import patch

from tags_counter import app, backend
from tags_counter.backend import mongo


class TestTagsApi(unittest.TestCase):

    def setUp(self):
        mongo.get_connection().drop_database('test')
        app.config['MONGODB_NAME'] = 'test'
        self.app = app.test_client()

    def test_add_invalid_url(self):
        """
        API должно вернуть bad request
        """
        response = self.app.post('/tags/',
                      data=json.dumps(dict(target_url='//invalid.com')),
                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_valid_url_1(self):
        """
        API должно успешно поставить задачу в очередь, и вернуть информацию о задаче.
        """
        response = self.app.post('/tags/',
                      data=json.dumps(dict(target_url='http://openflashcards.github.io')),
                      content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertListEqual(response_json['result'].keys(), ['state', 'target_url', 'task_id'])

    def test_get_valid_task(self):
        test_url = 'http://openflashcards.github.io'
        response_post = self.app.post('/tags/',
                      data=json.dumps(dict(target_url=test_url)),
                      content_type='application/json')
        response_post_json = json.loads(response_post.data.decode('utf-8'))
        task_id = response_post_json['result']['task_id']

        response_get = self.app.get('/tags/%s' % (task_id, ), )
        response_get_json = json.loads(response_post.data.decode('utf-8'))
        self.assertEqual(response_get.status_code, 200)
        self.assertDictEqual(response_get_json['result'], {'task_id': task_id, 'target_url': test_url, 'state': 'wait'})

    def test_get_unexisted_task(self):
        """
        API должно вернуть 404 на запрос несуществующего task-a
        """
        response_get = self.app.get('/tags/%s/' % ('la-la-la', ), )
        self.assertEqual(response_get.status_code, 404)
