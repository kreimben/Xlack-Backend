import logging

from fastapi import APIRouter, UploadFile, status, Depends
from sqlalchemy.orm import Session

from app.model.crud.channel import read_channel
from app.model.crud.file import create_file, read_file, read_files, update_file, delete_file
from app.model.crud.chat_history import create_history, delete_history, read_history
from app.model.database import get_db
from app.utils.jwt import check_auth_using_token
from app.utils.responses import SuccessResponse, FailureResponse

router = APIRouter(prefix='/file', tags=['File Upload'])


@router.post('/')
async def file_create(file: UploadFile,
                      channel_id: int,
                      db: Session = Depends(get_db)):
    logging.info('POST /file/')

    # Check `channel_id` is exists.
    if not await read_channel(db=db, channel_id=channel_id):
        return FailureResponse(message='Not those channel.', status_code=status.HTTP_404_NOT_FOUND)

    file_db = await create_file(db=db, file_name=file.filename, file=bytes(file.file))
    await create_history(db=db, channel_id=channel_id, file_id=file_db.file_id)

    return SuccessResponse(message='Successfully file created.',
                           status_code=status.HTTP_201_CREATED,
                           file=file_db.to_dict())


@router.get('/all')
async def file_all(db: Session = Depends(get_db)):
    logging.info('GET /file/all')
    files = await read_files(db=db)
    return SuccessResponse(files=[file.to_dict() for file in files])


@router.get('/{file_id}')
async def file_get(file_id: int,
                   db: Session = Depends(get_db)):
    logging.info('GET /file/{file_id}')

    file = await read_file(db=db, file_id=file_id)

    return SuccessResponse(file=file.to_dict())


@router.patch('/{file_id}')
async def file_update(file_id: int,
                      new_file: UploadFile,
                      db: Session = Depends(get_db)):
    logging.info('PATCH /file/{file_id}')

    rows = await update_file(db=db, file_id=file_id, file_name=new_file.filename, file=bytes(new_file.file))

    if rows == 1:
        return SuccessResponse(message='Successfully updated.', count=rows)
    else:
        return FailureResponse(message='Something is wrong!', count=rows, status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{file_id}')
async def file_delete(file_id: int,
                      db:Session=Depends(get_db)):
    logging.info('DELETE /file/{file_id}')

    rows = await delete_file(db=db, file_id=file_id)

    if rows == 1:
        return SuccessResponse(message='Successfully deleted.', count=rows)
    else:
        return FailureResponse(message='Something is wrong!', count=rows, status_code=status.HTTP_404_NOT_FOUND)

