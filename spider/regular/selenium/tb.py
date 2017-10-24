from selenium import webdriver
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pyq
from selenium.webdriver.support import expected_conditions as EC
import json

wdr = webdriver.Firefox()
wdr.get('https://www.taobao.com/')
wdr.find_element_by_id('q').send_keys('books')
wdr.find_element(By.CSS_SELECTOR, '.btn-search').click()
wdr.find_element(By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')
html =  pyq(wdr.page_source)
items = html('#mainsrp-itemlist .items .item').items()
for item in  items:
    product = {
        'image': item.find('.pic .img ').attr('src'),
        'price': item.find('.price').text(),
        'deal': item.find('.deal-cnt').text()[:-3],
        'title': item.find('.title').text(),
        'shop': item.find('.shop').text(),
        'location': item.find('.location').text(),
        'url': item.find('.pic .pic-link').attr('href')
    }
    print json.dumps(product, indent=4)
# wdr.close()
