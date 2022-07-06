from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, File, UploadFile, HTTPException
from datetime import datetime
from typing import Union
router = APIRouter(prefix='/channel', tags=['channel'])

"""Channels"""

class MyChannel(BaseModel):
    name: str | None = None
    id: int
    info: str | None = None

@router.get('/create_channel')
async def get_channel_info(channel_id: int, channel_name: str | None = "unnamed"):
    return {"channel_id": channel_id,
            "channel_name": channel_name}


@router.get('/create_channel/{channel_member}')
async  def get_channel_info(member_name: str):
    return {member_name}

@router.get('/create_channel/get_channel_info/{get_channel_feature}')
async def get_channel_feature(feature: None):
    return feature

@router.get('/create_channel/channel_info/{channel_date}')
async def get_channel_datetime(date: datetime):
    return date

@router.delete('/create_channel/{get_channel_info}')
async def delete_channel_info(member_name:str, member_profile: bytes = File()):
    member_name = get_channel_info.get(member_name)
    if member_name not in get_channel_info():
        raise HTTPException(status_code=404, datail = "404 not found")
    get_channel_info.delete(member_name)
    get_channel_info.commit()
    return{"deleted": True}

"""Chats"""

class Chat(BaseModel):
    chatter: str
    content: str
    date: datetime

@router.post('/create_chat', response_model=Chat)
async def create_chat(chat: Chat):
    return chat

@router.get('/create_chat/{show_chat}')
async def show_chat(chat: Chat):
    return{"content": Chat.content,
           "chatter": Chat.chatter,
           "date": Chat.date}

