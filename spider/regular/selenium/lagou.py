#!encoding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
wdr = webdriver.Firefox()
wdr.get('https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4%E5%B7%A5%E7%A8%8B%E5%B8%88?px=default&city=%E4%B8%8A%E6%B5%B7#filterBox')
wdr.find_element_by_id('search_butten').send_keys('运维工程师')
wdr.find_element_by_xpath('html body div#content-container div#main_container div.content_left div#s_position_list.s_position_list ul.item_con_list li.con_list_item.default_list div.list_item_top div.position div.p_top a.position_link h3').click()
# job_money = re.findall(wdr.page_source, 'data-salary="(.*?)"')
# job_compay = re.findall(wdr.page_source, 'data-compay="(.*?)"')
# job_list = re.findall(wdr.page_source, 'data-')
# jobs_list = re.findall(wdr.page_source, '<h3>(.*?)</h3>', re.S)
# print jobs_list
#wdr.find_element_by_id('img_out_754267513').click()
