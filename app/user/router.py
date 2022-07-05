from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..model.crud import user, authorization
from ..model.database import get_db
from ..model.schemas import UserCreate

router = APIRouter(tags=['user'])


@router.post('/user')
async def create_user(user_info: UserCreate,
                      db: Session = Depends(get_db)):
    # Check authorization first!
    if not await authorization.read_authorization(name=user_info.authorization, db=db):
        raise HTTPException(status_code=404, detail='No such authorization.')

    # If authorization exists, create user.
    result = await user.create_user(github_id=user_info.github_id,
                                    email=user_info.email,
                                    name=user_info.name,
                                    authorization_name=user_info.authorization,
                                    db=db)

    return {
        'success': True,
        'message': 'Successfully created user.',
        'user': result
    }


@router.get('/user')
async def read_user_info(db: Session = Depends(get_db)):
    return ''
