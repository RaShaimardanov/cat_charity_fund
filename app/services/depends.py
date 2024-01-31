from typing import Optional

from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.validators import CharityProjectValidator

from app.core.db import get_async_session
from app.models import Donation, CharityProject
from app.services import DonationService
from app.crud import charityproject_crud, donation_crud


async def get_donation_service(session: AsyncSession = Depends(get_async_session)):
    async def get_next_project() -> Optional[CharityProject]:
        return await charityproject_crud.get_next_charityproject_not_fully_invested(session)

    async def get_next_donation() -> Optional[Donation]:
        return await donation_crud.get_next_donate_not_fully_invested(session)

    return DonationService(get_next_project, get_next_donation, session)


async def get_project_validator(session: AsyncSession = Depends(get_async_session)) -> CharityProjectValidator:
    return CharityProjectValidator(session)
