from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

#playwright→BeautifulSoup4→pandasでHTMLのtableを読み込む
def get_html(playwright):
    try:
        #playwright
        browser = playwright.firefox.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.wise-agent.com/database/")
        html = page.content()
        #print(f'html:{html}')
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)
        title_text = soup.find('title').get_text()
        print(title_text)
        print('###########################################################')

        links = [url.get('href') for url in soup.find_all('a')]
        result_link = []
        for i in links:
            print(i)
            if i.startswith('/') or len(i) <= 27 or i in '.html':
                pass
            else:
                result_link.append(i)
        for i in result_link:
            print(i)

#            page.goto("https://www.wise-agent.com/database/")
#            page.get_by_role("link",    name="【IN    GROUPE】高林イツキに関する情報提供").nth(1).click()
#            page.get_by_text("情報商材    2021.04.08    【IN    GROUPE】高林イツキに関する情報提供    詐欺種別    情報商材    名称等    IN    GROUPE    LUC888&evolutio").click()
#            #    BeautifulSoup4
#            soup    =    BeautifulSoup(html,    "lxml")
#            tables    =    soup.find_all("table")
#            print(tables)
        #    pandas
        #            dfs    =    pd.read_html(str(tables))

    except:
        #エラー処理を書く（HTTPエラー、tableタグなし等）
        print("Error")

#        else:
#            #    pandasのデータフレーム処理を書く
#            #            print(dfs)

    finally:
        page.close()
        context.close()
        browser.close()

#    get_html関数呼び出し
with sync_playwright() as playwright:
    get_html(playwright)