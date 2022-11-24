from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from models import *
from flask import Flask

#engine = create_engine("postgresql://postgres:30062003@localhost:5432/cinema", echo=True)
engine = create_engine("postgresql://postgres:postgres22@localhost:5432/cinema", echo=True)

metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()
