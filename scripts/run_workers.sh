#!/usr/bin/env bash
celery -A tags_counter.celery_app worker
