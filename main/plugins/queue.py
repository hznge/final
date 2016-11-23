#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from celery import Celery


def make_celery(app):
    """
    integrate Celery with Flask
    http://flask.pocoo.org/docs/0.11/patterns/celery/#configuring-celery
    """
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKEN_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
