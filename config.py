from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv
from typing import Final


#DBとの接続のための設定
load_dotenv()
SQLALCHEMY_DATABASE_URI: Final = "{dialect}+{driver}://{username}:{password}@{host}/{database}".format(
    dialect=os.getenv('DIALECT'),
    driver=os.getenv('DRIVER'),
    username=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    host=os.getenv('HOST', 'localhost'),
    database=os.getenv('DATABASE'),
)

#Engineの作成
engine: Engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

#sessionの作成
session: scoped_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

#テーブルを作成するための初期化のようなもの
Base = declarative_base()
Base.query = session.query_property()
