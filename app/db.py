from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from pprogram.models import *

engine = create_engine("postgresql://postgres:30062003@localhost:5432/cinema", echo=True)

metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()
