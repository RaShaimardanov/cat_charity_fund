from sqlalchemy import Column, Text, Integer, ForeignKey


from app.core.db import Base
from app.models.base import BaseModelMixin


class Donation(BaseModelMixin, Base):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey(
        'user.id', name='fk_reservation_user_id_user')
    )
