from fastapi import FastAPI, Request, Cookie
from app.ready import ready_app
import uvicorn

app: FastAPI = ready_app()


@app.get('/hello/{user_id}', tags=['hi'])
async def hello(user_id: str, some_query: str, request: Request, anything: str | None = Cookie(None)):
    return {
        'success': True,
        'user_id': user_id,
        'some_query': some_query,
        'base_url': request.base_url,
        'cookie_anything': anything
    }

@app.patch('/sldkfjlsdkj/sdgsdg')
async def hihihihi():
    return 'hi'



@app.delete('/sldkfjsldkj')
async def sldkj():
    return 'sdglkjsdlfkj'


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8080, reload=True, log_level='info')
