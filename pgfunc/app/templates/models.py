from sqlalchemy import Column, Integer, String
from ..dao.database import Base

class Item(Base):
    __tablename__ = "items"
    __table_args__ = {'schema': 'tgabm00'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
