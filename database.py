from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func,Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///gaozhong.sqlite?check_same_thread=False')


class GaoZhong(Base):
    __tablename__ = 'gaozhong'
    id = Column(Integer, primary_key=True)
    province_name = Column(String)
    province_code = Column(String)
    city_name = Column(String)
    city_code = Column(String)
    area_name = Column(String)
    area_code = Column(String)
    school_name = Column(String)
    shool_code = Column(String)



Base.metadata.create_all(engine)