from selenium import webdriver
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pyq
from selenium.webdriver.support import expected_conditions as EC
import json

wdr = webdriver.Firefox()
wdr.get('http://www.jikexueyuan.com/')
wdr.find_element(By.CSS_SELECTOR, '#searchinput').send_keys('hadoop')
wdr.find_element(By.CSS_SELECTOR, '#search-bottom').click()
html = pyq(wdr.page_source)
course = html.find('.leftarea ul li')
for item in course.items():
    coursech = item.find('.info').items()
    for itemch in coursech:
        # print itemch
        # print itemch.find('.info a').attr('href')
        # break
        kelist = {
            'title': itemch.find('.title').text(),
            'desc': itemch.find('.description').text(),
            'URL': itemch.find('.info a').attr('href')
        }
        print json.dumps(kelist, indent=4)
    break
wdr.close()