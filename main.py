from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text, DateTime, Date
from sqlalchemy.sql.functions import current_timestamp
from datetime import datetime


with sync_playwright() as playwright:
    SQLALCHEMY_DATABASE_URI = "{dialect}+{driver}://{username}:{password}@{host}/{database}".format(
        dialect='mysql',
        driver='pymysql',
        username='root',
        password='123abc',
        host='localhost',
        database='scraping',
    )

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    #sessionの作成
    session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    )

    #テーブルの定義
    Base = declarative_base()
    Base.query = session.query_property()

    class Fraud(Base):
        __tablename__ = 'frauds'
        id = Column(Integer, primary_key=True, nullable=False, unique=True)
        created_at=Column(DateTime, server_default=current_timestamp(), nullable=False)
        category = Column(Text, nullable=False, unique=False)
        date = Column(Date, nullable=False, unique=False)
        title = Column(Text, nullable=False, unique=False)
        type_of_fraud = Column(Text, nullable=False, unique=False)
        name = Column(Text, nullable=False, unique=False)
        location = Column(Text, nullable=False, unique=False)
        representative = Column(Text, nullable=False, unique=False)
        phone_number = Column(Text, nullable=False, unique=False)
        email = Column(Text, nullable=False, unique=False)
        url = Column(Text, nullable=False, unique=False)
        content = Column(Text, nullable=False, unique=False)
        def __init__(self, category, date, title,  type_of_fraud=None, name=None, location=None, representative=None, phone_number=None, email=None, url=None, content=None):
            self.category = category
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

    try:
        #playwright
        browser = playwright.firefox.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.wise-agent.com/database/")
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        #TODO: classで絞ってから持ってくる
        db_components = soup.find_all('div', {'class': 'businessbox-db-text'})

        def get_link(db_components: List[str]):
            links: List[str] = []
            for i in range(len(db_components)):
                for url in db_components[i].find_all('a'):
                    links.append(url.get('href'))
            return links

        links = get_link(db_components=db_components)

        for i in links:
            page.goto(i)
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            print('----------------------------------------------------')
            print('headingの内容++++++++++++++++++++++++++++++++++++++++')
            #TODO: headingの内容
            post_title = soup.find_all('div', {'class': 'post-title'})
            post_title = post_title[0]
            post_title_category = post_title.find('div', {'class': 'category'}).text
            post_title_date = post_title.find('div', {'class': 'date'}).text
            post_title_title = post_title.select('div > div:nth-of-type(3)')[0].text

            #datetime変換
            post_title_date =datetime.strptime(post_title_date, '%Y.%m.%d')
            post_title_date = post_title_date.date()

            #確認用
            # print(f'{post_title.prettify()}')
            print(f'post_title_category: {post_title_category}')
            print(f'post_title_date: {post_title_date}')
            print(f'post_title_title: {post_title_title}')
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('tableの内容+++++++++++++++++++++++++++++++++++++++++++')
            post_table = soup.find_all('tbody')
            post_table = post_table[0]
            post_table_type_of_fraud = post_table.select('tbody > tr:nth-of-type(1) > td')[0].text
            post_table_name = post_table.select('tbody > tr:nth-of-type(2) > td')[0].text
            post_table_location = post_table.select('tbody > tr:nth-of-type(3) > td')[0].text
            post_table_representative = post_table.select('tbody > tr:nth-of-type(4) > td')[0].text
            post_table_phone_number = post_table.select('tbody > tr:nth-of-type(5) > td')[0].text
            post_table_email = post_table.select('tbody > tr:nth-of-type(6) > td')[0].text
            post_table_url = post_table.select('tbody > tr:nth-of-type(7) > td')[0].text
            post_table_content = post_table.select('tbody > tr:nth-of-type(8) > td')[0]

            #確認用
            # print(f'{post_table.prettify()}')
            print(f'詐欺種別: {post_table_type_of_fraud}')
            print(f'名称等: {post_table_name}')
            print(f'所在地: {post_table_location}')
            print(f'代表者: {post_table_representative}')
            print(f'電話番号: {post_table_phone_number}')
            print(f'E-mail: {post_table_email}')
            print(f'URL: {post_table_url}')
            print(f'{post_table_content.prettify()}')
            post_table_content = str(post_table_content)
            print(type(post_table_content))

            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('----------------------------------------------------')
            #データベースに保存
            #INSERT
            row = Fraud(
                category = post_title_category,
                date = post_title_date,
                title = post_title_title,
                type_of_fraud=post_table_type_of_fraud,
                name=post_table_name,
                location=post_table_location,
                representative=post_table_representative,
                phone_number=post_table_phone_number,
                email=post_table_email,
                url=post_table_url,
                content=post_table_content
            )
            session.add(row)
            session.commit()
    except:
        print('Error')
    finally:
        page.close()
        context.close()
        browser.close()
