import pymysql
from sqlalchemy import Integer, Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import Config

pymysql.install_as_MySQLdb()

engine = create_engine(f'mysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(20), unique=True)
    email = Column('email', String(20), unique=True)
    password = Column('password', String(256))
    index = Column('index', String(40), unique=True)


class AccountToken(Base):
    __tablename__ = 'account_token'
    account_id = Column('account_id', Integer, primary_key=True)
    token = Column('token', String(30), unique=True)
    update_date = Column('update_date', DateTime)
