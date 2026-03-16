from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    status = Column(String, default="UNKNOWN")
    response_time = Column(Float, nullable=True)