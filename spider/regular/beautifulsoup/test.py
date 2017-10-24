from selenium import webdriver
wdr = webdriver.Firefox()
wdr.get("http://ui.ptlogin2.qq.com/cgi-bin/login?style=9&appid=30000101&low_login=0&hln_css=http%3A%2F%2Fmat1.gtimg.com%2Fgongyi%2Fm%2Fhtml5%2Flogo_login.png&s_url=http%3A%2F%2Fssl.gongyi.qq.com%2Fm%2Fweixin%2Fyqj_main.html%3Fid%3D415%26did%3D1214042801201708224500020050%26ADTAG%3Dqrcode")
wdr.find_element_by_id('u').send_keys("754267513")
wdr.find_element_by_id('p').send_keys("asdsadsd546")
wdr.find_element_by_id('go').click()
print wdr.page_source