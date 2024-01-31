from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charityproject_crud
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.api.validators import CharityProjectValidator
from app.services import (
    DonationService, get_donation_service, get_project_validator
)
from app.schemas.charityproject import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    donation_service: DonationService = Depends(get_donation_service),
    validator: CharityProjectValidator = Depends(get_project_validator)
):
    """
    Только для суперпользователя.
    Создать благотворительный проект.
    """
    await validator.check_name_duplicate(obj_in.name)
    new_charityproject = await charityproject_crud.create(obj_in, session)
    await donation_service.process_donations()
    await session.refresh(new_charityproject)
    return new_charityproject


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех проектов."""
    return await charityproject_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def charity_project_update(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    validator: CharityProjectValidator = Depends(get_project_validator)
):
    """
    Только для суперюзеров.
    Редактировать проект.
    Закрытый проект нельзя редактировать, также нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await validator.validate_update(project_id, obj_in)
    return await charityproject_crud.update(charity_project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def charity_project_delete(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    validator: CharityProjectValidator = Depends(get_project_validator)
):
    """
    Только для суперюзеров.
    Удалить проект.
    Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.
    """
    charity_project = await validator.validate_delete(project_id)
    return await charityproject_crud.remove(charity_project, session)
