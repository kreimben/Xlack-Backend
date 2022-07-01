from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/test')
async def test(hi: str | None = None):
    return {
        'success': True,
        'hi': hi
    }
