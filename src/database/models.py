from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(25), nullable=False, index=True)
    last_name = Column(String(25), nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, unique=True, index=True)
    birthday = Column(DateTime, default=None, index=True)

