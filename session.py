from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

engine = create_engine('sqlite:///gaozhong.sqlite?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()