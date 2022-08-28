#!/usr/bin/env python
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))
    
has_celery = '{{ cookiecutter.need_celery }}'

if __name__ == '__main__':

    if  not has_celery:
        remove_file('config/worker.py')
        remove_file('Dockerfile.worker')
