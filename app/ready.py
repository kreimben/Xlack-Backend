import logging
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.model.database as database


def ready_for_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('all.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def ready_for_db():
    database.Base.metadata.create_all(bind=database.engine)
    logging.debug(f'Ready for db!')


def ready_app() -> FastAPI:
    ready_for_db()
    ready_for_logging()

    app = FastAPI(
        title='Xlack',
        description='Furthermore Workspace.',
        version='0.2.0'
    )

    origins = [
        '*'
        'localhost',
        'http://localhost',
        'localhost:3000',
        'http://localhost:3000'
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    is_debugging = os.getenv('IS_DEBUGGING')
    if not bool(is_debugging if is_debugging is not None else False):
        logging.info(f'DEPLOY MODE.')
        app.root_path = '/api'

    return app
