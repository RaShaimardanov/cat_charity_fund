from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_property


class BaseModelMixin(object):
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=lambda: datetime.now())
    close_date = Column(DateTime, default=None)

    @hybrid_property
    def remainder_amount(self) -> int:
        return self.full_amount - self.invested_amount
