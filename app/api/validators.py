from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.crud.charityproject import charityproject_crud


class CharityProjectValidator:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate_update(self, project_id: int, data: dict):
        project = await self.check_charity_project_exists(project_id)
        await self.check_name_duplicate(data.name)
        await self.check_close_project(project)
        if data.full_amount:
            await self.check_project_sum_invested(project, data.full_amount)
        return project

    async def validate_delete(self, project_id: int):
        project = await self.check_charity_project_exists(project_id)
        await self.check_project_invested(project)
        return project

    async def check_charity_project_exists(
            self,
            project_id: int,
    ) -> CharityProject:
        charity_project = await charityproject_crud.get(
            project_id, self.session
        )
        if charity_project is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Проект не найден!'
            )
        return charity_project

    async def check_name_duplicate(
            self,
            project_name: str,
    ) -> None:
        project_id = await charityproject_crud.get_charityproject_id_by_name(
            project_name, self.session
        )
        if project_id is not None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Проект с таким именем уже существует!',
            )

    async def check_project_invested(self, project) -> None:
        if project.invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='В проект были внесены средства, не подлежит удалению!',
            )

    async def check_project_sum_invested(self, project, amount: int) -> None:
        if project.invested_amount > amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Требуемая сумма меньше внесённой!',
            )

    async def check_close_project(self, project) -> None:
        if project.fully_invested:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Закрытый проект нельзя редактировать!',
            )
