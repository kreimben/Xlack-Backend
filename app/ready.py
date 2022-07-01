from fastapi import FastAPI


def ready_app() -> FastAPI:
    app = FastAPI(
        title='Xlack',
        description='Furthermore Workspace.',
        version='0.1.0'
    )
    return app
