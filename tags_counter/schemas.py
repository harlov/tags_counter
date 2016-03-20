# -*- coding: utf-8 -*-
"""
Схема задачи
"""
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class TagsTaskSchema(Schema):
    """
    Schema for tags count task.
    """
    STATE_WAIT = 'wait'
    STATE_RUN = 'run'
    STATE_DONE = 'done'
    STATE_ERROR = 'error'
    STATE_CHOICES = (STATE_WAIT, STATE_RUN, STATE_DONE, STATE_ERROR)

    target_url = fields.Url(required=True)
    task_id = fields.Str()
    state = fields.Str(validate=OneOf(STATE_CHOICES), default=STATE_WAIT, missing=STATE_WAIT)
    result = fields.Str()


TAGS_TASK_SCHEMA = TagsTaskSchema()

