from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_next_donate_not_fully_invested(
            self,
            session: AsyncSession,
    ) -> Donation:
        db_donation = await session.execute(
            select(Donation).where(
                ~Donation.fully_invested
            ).order_by(Donation.create_date.asc())
        )
        return db_donation.scalars().first()

    async def get_all_donations_user(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        db_donats = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_donats.scalars().all()


donation_crud = CRUDDonation(Donation)