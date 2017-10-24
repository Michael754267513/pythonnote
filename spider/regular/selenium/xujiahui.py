from selenium import webdriver
wdr = webdriver.Firefox()
wdr.get('http://www.pre.xjh.com/')
wdr.find_element_by_id('login').click()
wdr.find_element_by_id('userName').send_keys("18500197165")
wdr.find_element_by_id('password').send_keys("111111")
wdr.find_element_by_class_name('login_button').click()
