from fastapi import FastAPI


def ready_app() -> FastAPI:
    app = FastAPI()
    return app
