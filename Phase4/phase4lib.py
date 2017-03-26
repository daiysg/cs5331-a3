#datamatch = [ 
#		{"//div[@class='div8']" : "selector" },
#		{"//div[@class='abc']" : "defghil" },
#		{"//div[@class='selected']//a/text()" : "US Dollar"}
#	]

# @ just to check if the login is passed
def check_login(html_body, cur_url, login_url):
	if (html_body.lower().find('login') >= 0):
		print 'Login found'
		return True
	if (cur_url == login_url):
		print 'Login Url and cur url are the same'
		return True
	if (cur_url.lower().find('login') >= 0):
		print 'current url has login in url'
		return True

	return False

# @ update the pass/fail results in a log file
def update_results(result_string):
	file = open("output.log", 'a')
	file.write(result_string)
	file.close();