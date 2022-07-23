import logging
import uuid

from sqlalchemy.orm import Session

from app.model import models


async def create_file(db: Session, file_name: str, file: bytes) -> models.File:
    file = models.File(uuid=str(uuid.uuid4()),
                       file_name=file_name,
                       file_binary=bytes(file))
    logging.debug(f'file: {file.to_dict()}')
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


async def read_file(db: Session, file_id: int) -> models.File:
    file = db.query(models.File).filter(models.File.file_id == file_id).first()
    logging.debug(f'file: {file.to_dict()}')
    return file


async def read_files(db: Session) -> [models.File]:
    files = db.query(models.File).all()
    logging.debug(f'files: {files.to_dict()}')
    return files


async def update_file(db: Session, file_id: int, file_name: str, file: bytes) -> int:
    rows = db.query(models.File) \
        .filter(models.File.file_id == file_id) \
        .update({'file_name': file_name,
                 'file_binary': file})
    db.commit()
    return rows


async def delete_file(db: Session, file_id: int) -> int:
    rows = db.query(models.File).filter(models.File.file_id == file_id).delete()
    db.commit()
    return rows
