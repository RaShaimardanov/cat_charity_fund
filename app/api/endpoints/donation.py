from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.core.user import current_user, current_superuser
from app.services import DonationService, get_donation_service
from app.schemas.donation import DonationCreate, DonationDB, DonationAdminDB

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_new_donation(
        obj_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        donation_service: DonationService = Depends(get_donation_service),
        user: User = Depends(current_user)
) -> DonationDB:
    """
    Сделать пожертвование.
    """
    new_donation = await donation_crud.create(obj_in, session, user)
    await donation_service.process_donations()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationAdminDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session)
) -> list[DonationAdminDB]:
    """
    Только для суперпользователя.
    Получить список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model_exclude_none=True,
    response_model=list[DonationDB]
)
async def get_user_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> list[DonationDB]:
    """
    Получить список пожертвований пользователя.
    """
    return await donation_crud.get_all_donations_user(session, user)
