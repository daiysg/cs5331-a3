# @ just to check if the login is passed
def check_login(html_body, cur_url, login_url):
    if cur_url == login_url:
        return True
    else:
        return False


# @ update the pass/fail results in a log file
def update_results(result_string):
    update_file = open("output.log", 'a')
    update_file.write(result_string)
    update_file.close();
