from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    status = Column(String, default="UNKNOWN")
    response_time = Column(Float, nullable=True)


class ServiceCheck(Base):
    __tablename__ = "service_checks"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    status = Column(String, nullable=False)
    response_time = Column(Float, nullable=True)
    checked_at = Column(String, nullable=False)