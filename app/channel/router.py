from fastapi import APIRouter

router = APIRouter(prefix='/channel', tags=['channel'])


@router.get('/test')
async def test_code(hi: str | None = None):
    return {
        'success': True,
        'hi': hi
    }
