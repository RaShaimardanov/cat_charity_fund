from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charityproject_id_by_name(
            self,
            charityproject: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charityproject_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charityproject
            )
        )
        return db_charityproject_id.scalars().first()

    async def get_next_charityproject_not_fully_invested(
            self,
            session: AsyncSession,
    ) -> CharityProject:
        db_charityproject = await session.execute(
            select(CharityProject).where(
                ~CharityProject.fully_invested
            ).order_by(CharityProject.create_date.asc())
        )
        return db_charityproject.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)
