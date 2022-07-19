import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.model.crud.authorization import read_authorization, delete_authorization, update_authorization, \
    create_authorization, read_authorizations
from app.model.database import get_db
from app.utils.responses import FailureResponse, SuccessResponse

router = APIRouter(prefix='/authorization', tags=['authorization'])


@router.post('/')
async def create_auth(name: str = Query(max_length=25), db: Session = Depends(get_db)):
    logging.info('POST /authorization/')
    auth = await read_authorization(name, db)
    if auth:
        logging.debug(f'Authorization Already Exists: {auth.name}')
        return FailureResponse(message='Already exists.', authorization=auth, status_code=status.HTTP_404_NOT_FOUND)
    else:
        auth = await create_authorization(name, db)
        logging.debug(f'Authorization Successfully Created: {auth.name}')
        return SuccessResponse(message='Successfully authorization created.', authorization=auth.to_dict())


@router.get('/')
async def get_auth(name: str, db: Session = Depends(get_db)):
    logging.info('GET /authorization/')
    auth = await read_authorization(name, db)
    logging.debug(f'auth: {auth}')

    if auth is not None:
        return SuccessResponse(authorization=auth.to_dict())
    else:
        return FailureResponse(message='No such authorization.', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/all')
async def get_all_auth(db: Session = Depends(get_db)):
    logging.info('GET /authorization/all')
    auths = await read_authorizations(db)
    logging.debug(f'auths: {auths}')

    if len(auths) != 0:
        return SuccessResponse(data=[auth.to_dict() for auth in auths])
    else:
        return FailureResponse(message='No authorizations.', status_code=status.HTTP_404_NOT_FOUND)


@router.patch('/')
async def update_auth(old_name: str = Query(max_length=25),
                      new_name: str = Query(max_length=25),
                      db: Session = Depends(get_db)):
    logging.info('PATCH /authorization/')
    auth = await update_authorization(old_name=old_name, new_name=new_name, db=db)
    logging.debug(f'auth: {auth}')

    if auth != 0:
        auth = await read_authorization(name=new_name, db=db)
        return SuccessResponse(message='Successfully changed.', authorization=auth.to_dict())
    else:
        return FailureResponse(message='No such authorization.', status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/')
async def delete_auth(name: str,
                      db: Session = Depends(get_db)):
    logging.info('DELETE /authorization/')
    rows = await delete_authorization(name, db)
    logging.debug(f'deleted auth: {rows}')

    if rows != 0:
        return SuccessResponse(count=rows, message='Successfully Deleted.')
    else:
        return FailureResponse(message='No such authorization.', status_code=status.HTTP_404_NOT_FOUND)
