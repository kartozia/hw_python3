import lxml
#from lxml import etree
class Article:
    def __init__(self, title, date):
        self.title = title
        self.date = date
        
    def __str__(self):
        return self.title + ' [' + self.date + ']'

# скачиваем главную страницу Хабрахабра
import requests
page = requests.get('https://habrahabr.ru/')

print(page.text[:251]) # в атрибуте text  можно посмотреть текст страницы, которая скачалась
