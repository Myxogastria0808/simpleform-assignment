from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text, DateTime, Date
from sqlalchemy.sql.functions import current_timestamp
from config import Base, engine
import datetime


class Fraud(Base):
    __tablename__ :str = 'frauds'
    id: Column[int] = Column(Integer, primary_key=True, nullable=False, unique=True)
    created_at: Column[datetime.datetime] =Column(DateTime, server_default=current_timestamp(), nullable=False)
    date: Column[datetime.date] = Column(Date, nullable=False, unique=False)
    title: Column[str] = Column(Text, nullable=False, unique=False)
    type_of_fraud: Column[str] = Column(Text, nullable=False, unique=False)
    name: Column[str] = Column(Text, nullable=False, unique=False)
    location: Column[str] = Column(Text, nullable=False, unique=False)
    representative: Column[str] = Column(Text, nullable=False, unique=False)
    phone_number: Column[str] = Column(Text, nullable=False, unique=False)
    email: Column[str] = Column(Text, nullable=False, unique=False)
    url: Column[str] = Column(Text, nullable=False, unique=False)
    content: Column[str] = Column(Text, nullable=False, unique=False)
    def __init__(self, date, title,  type_of_fraud=None, name=None, location=None, representative=None, phone_number=None, email=None, url=None, content=None):
        self.date = date
        self.title = title
        self.type_of_fraud = type_of_fraud
        self.name = name
        self.location = location
        self.representative = representative
        self.phone_number = phone_number
        self.email = email
        self.url = url
        self.content = content
#テーブルの生成
Base.metadata.create_all(bind=engine)

