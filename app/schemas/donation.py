from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    id: int
    create_date: datetime


class DonationAdminDB(DonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
