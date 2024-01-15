from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, Integer, DateTime, Float

metadata = MetaData()

data_respondent = Table(
    "data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", DateTime),
    Column("respondent", Integer),
    Column("sex", Integer),
    Column("age", Integer),
    Column("weight", Float),

)


class Audience(BaseModel):
    audience1: str
    audience2: str
