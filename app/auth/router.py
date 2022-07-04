from fastapi import APIRouter
from ..model.crud import user, authorization

router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/redirect/github')
async def redirect_github():
    """
    This function deal with after redirect from client.

    :return:
    """
    return ''
