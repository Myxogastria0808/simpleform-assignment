from bs4 import BeautifulSoup, ResultSet
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import List, Dict, Union
from datetime import datetime
from models import Fraud
from config import session
import json


with sync_playwright() as playwright:
    try:
        #https://www.wise-agent.com/database/にアクセス (playwrightの処理)
        browser: Browser = playwright.firefox.launch()
        context: BrowserContext = browser.new_context()
        page: Page = context.new_page()
        page.goto("https://www.wise-agent.com/database/")
        html: str = page.content()
        #BeautifulSoupに渡している
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        
        #目的のhtmlの要素を絞っている
        db_components: ResultSet = soup.find_all('div', {'class': 'businessbox-db-text'})

        #各詳細リンクを回収する関数の定義
        def get_link(db_components: List[str]) -> List[str]:
            links: List[str] = []
            for i in range(len(db_components)):
                for url in db_components[i].find_all('a'):
                    links.append(url.get('href'))
            return links
        #各詳細リンクを回収する関数の実行
        links: List[str] = get_link(db_components=db_components)

        #前回のデータの行数を取得
        old_column_number: int = session.query(Fraud.id).count()

        #各詳細ページでの処理
        for i in links:
            #各詳細ページにアクセス (playwrightの処理)
            page.goto(i)
            #目的のhtml要素の取得
            html: str = page.content()
            soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
            print('----------------------------------------------------')
            print('headingの内容++++++++++++++++++++++++++++++++++++++++')
            #heading要素の内容を取得
            post_title: ResultSet = soup.find_all('div', {'class': 'post-title'})
            post_title: ResultSet = post_title[0]
            post_title_date: str = post_title.find('div', {'class': 'date'}).text
            post_title_title: str = post_title.select('div > div:nth-of-type(3)')[0].text

            #datetime.date型に変換
            post_title_date: datetime =datetime.strptime(post_title_date, '%Y.%m.%d')
            post_title_date: datetime = post_title_date.date()

            #scraping.log出力用
            print(f'post_title_date: {post_title_date}')
            print(f'post_title_title: {post_title_title}')
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('tableの内容+++++++++++++++++++++++++++++++++++++++++++')
            #table要素の内容を取得
            post_table: ResultSet = soup.find_all('tbody')
            post_table: ResultSet = post_table[0]
            post_table_type_of_fraud: str = post_table.select('tbody > tr:nth-of-type(1) > td')[0].text
            post_table_name: str = post_table.select('tbody > tr:nth-of-type(2) > td')[0].text
            post_table_location: str = post_table.select('tbody > tr:nth-of-type(3) > td')[0].text
            post_table_representative: str = post_table.select('tbody > tr:nth-of-type(4) > td')[0].text
            post_table_phone_number: str = post_table.select('tbody > tr:nth-of-type(5) > td')[0].text
            post_table_email: str = post_table.select('tbody > tr:nth-of-type(6) > td')[0].text
            post_table_url: str = post_table.select('tbody > tr:nth-of-type(7) > td')[0].text
            post_table_content: ResultSet = post_table.select('tbody > tr:nth-of-type(8) > td')[0]

            #scraping.log出力用
            print(f'詐欺種別: {post_table_type_of_fraud}')
            print(f'名称等: {post_table_name}')
            print(f'所在地: {post_table_location}')
            print(f'代表者: {post_table_representative}')
            print(f'電話番号: {post_table_phone_number}')
            print(f'E-mail: {post_table_email}')
            print(f'URL: {post_table_url}')
            print(f'{post_table_content.prettify()}')

            #str型に変換
            post_table_content: str = str(post_table_content)
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('----------------------------------------------------')
            #データベースに保存
            row = Fraud(
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
        #今回取得されたデータより前にあった分のデータの削除
        data: Fraud = session.query(Fraud).first()
        for i in range(old_column_number):
            session.query(Fraud).filter(Fraud.id == data.id + i).delete()
            session.commit()
        new_data: List[Fraud] = session.query(Fraud).all()
        new_column_number: int = session.query(Fraud.id).count()

        #jsonファイルにデータを書き出し
        with open('api/jsonFiles/data.json', 'w') as data_file:
            data_list: List[Dict[str, Union[int, str]]] = []
            for i in range(new_column_number):
                data_list.append(
                    {
                        'id': new_data[i].id, 
                        'created_at': str(new_data[i].created_at),
                        'date': str(new_data[i].date), 
                        'title': new_data[i].title, 
                        'type_of_fraud': new_data[i].type_of_fraud, 
                        'name': new_data[i].name, 
                        'location': new_data[i].location, 
                        'representative': new_data[i].representative, 
                        'phone_number': new_data[i].phone_number, 
                        'email': new_data[i].email, 
                        'url': new_data[i].url, 
                        'content': new_data[i].content,
                    }
                )
            data_file.write(json.dumps({"data": data_list}))
    except Exception as e:
        print(e)
    finally:
        page.close()
        context.close()
        browser.close()
