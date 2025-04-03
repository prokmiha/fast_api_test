from .base import Base
from sqlalchemy import Integer, Float, String, Column, Date, ForeignKey

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    login = Column(String(100))
    registration_date = Column(Date)

class Credit(Base):
    __tablename__ = "credits"
    
    id = Column(Integer, primary_key=True)  
    user_id = Column(Integer, ForeignKey("users.id"))
    issuance_date = Column(Date)
    return_date = Column(Date)
    actual_return_date = Column(Date, nullable=True)
    body = Column(Float)
    percent = Column(Float)

class Dictionary(Base):
    __tablename__ = "dictionary"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True)
    period = Column(Date, default=1)
    total_sum = Column(Float)
    category_id = Column(Integer, ForeignKey("dictionary.id"))

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    sum = Column(Float)
    payment_date = Column(Date)
    credit_id = Column(Integer, ForeignKey("credits.id"))
    type_id = Column(Integer, ForeignKey("dictionary.id"))