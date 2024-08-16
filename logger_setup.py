#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Description of a global logging settings."""
import pathlib
import logging
import logging.config


ROOT_DIR = pathlib.Path.cwd()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'parser': {
            'class': 'logging.FileHandler',
            'filename': ROOT_DIR.joinpath('parser.log'),
            'formatter': 'parser',
            'level': 'INFO',
            'mode': 'a'
            },
    },
    'formatters': {
        'parser': {
            'format': '[%(levelname)s: %(asctime)s] [Class - %(name)s]\n %(message)s\n',
        },
    },
    'loggers': {
        'celery_app': {
            'level': 'INFO',
            'handlers': ['parser'],
            'propagate': False
        },
    }
}

logging.config.dictConfig(LOGGING)
