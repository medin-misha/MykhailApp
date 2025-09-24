from fastapi import APIRouter, Depends
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.user import CreateUser, ReturnUser
from services.user import UserCrud

router = APIRouter(tags=["http user"], prefix="/users")
