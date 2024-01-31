from datetime import datetime
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


class DonationService:
    def __init__(
            self,
            get_next_project: Callable[[AsyncSession], Optional[CharityProject]],
            get_next_donation: Callable[[AsyncSession], Optional[Donation]],
            session: AsyncSession
    ):
        self.get_next_project = get_next_project
        self.get_next_donation = get_next_donation
        self.session = session

    async def process_donations(self):
        project = await self.get_next_project()
        donation = await self.get_next_donation()

        if project and donation:
            investing_amount = min(donation.remainder_amount, project.remainder_amount)

            await self.update_obj(donation, investing_amount)
            await self.update_obj(project, investing_amount)

            await self.session.commit()

            await self.process_donations()

    async def update_obj(self, obj, investing_amount: int):
        obj.invested_amount += investing_amount
        if obj.remainder_amount == 0:
            obj.fully_invested = True
            obj.close_date = datetime.now()

        self.session.add(obj)
