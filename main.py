import os

import uvicorn
from fastapi import FastAPI

from app.authentication.router import router as authentication
from app.authorization.router import router as authorization_router
from app.channel.router import router as channel_router
from app.chat.router import router as chat_router
from app.ready import ready_app
from app.user.router import router as user_router

app: FastAPI = ready_app()

app.include_router(authentication)
app.include_router(channel_router)
app.include_router(user_router)
app.include_router(authorization_router)
app.include_router(chat_router)

if __name__ == '__main__':
    is_debugging = os.getenv('IS_DEBUGGING')
    is_debugging = bool(is_debugging if is_debugging is not None else False)
    uvicorn.run(app='main:app', host='0.0.0.0', port=8080, reload=is_debugging, log_level='info')
