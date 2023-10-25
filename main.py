from bs4 import BeautifulSoup
html_doc = '<html><head><title>タイトル</title></head><body><h1>見出し</h1></body></html>'
soup = BeautifulSoup(html_doc, 'html.parser')
print('title: ', soup.title.string)
print('h1: ', soup.body.h1.string)