#!/usr/bin/env python
import os
import time
import json
import copy
import itertools as it
import random

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from selenium import webdriver

from webcrawler.spiders.spider import StackSpider
from webcrawler.settings import process_link_value

from urls import URLs


## logging
def log_phase(num, desc):
    print
    print "{0} PHASE {1} {2}".format("#"*10, num, "#"*10)
    print "{0} {1} {2}".format("#"*2, desc, "#"*2)
    print

def log(msg):
    print msg


## Phase functions
def phase1():
    log_phase(1, "Crawling sites from urls.py for injection points.")

    log("Launching Chrome for selenium.")
    chromedriver = "/usr/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)
    time.sleep(3) # wait for firefox to open()

    settings = get_project_settings()

    # set logging output
    # clear log
    logfile = "scrapy_output.log"
    with open(logfile, 'w'):
        pass
    settings.set('LOG_ENABLED', True)
    settings.set('LOG_FILE', logfile)
    configure_logging(settings)
    log("Writing log to '{0}', tail it to follow process.".format(logfile))

    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        from urls import URLs
        from urls import crawl_rules_allow, crawl_rules_deny

        urlsItems = copy.deepcopy(URLs).items()

        log("Crawling URL items Size:'{0}'".format(urlsItems.__len__()))
        for urldata in urlsItems:
            # set site specific rules 
            data = urldata[1]
            if "crawl_rules_allow" in data:
                crawl_rules_allow = data["crawl_rules_allow"]
            else:
                data["crawl_rules_allow"] = crawl_rules_allow
            if "crawl_rules_deny" in data:
                crawl_rules_deny = data["crawl_rules_deny"]
            else:
                data["crawl_rules_deny"] = crawl_rules_deny

            log("Crawling '{0}'...".format(data["name"]))
            yield runner.crawl(StackSpider,
                               urldata=urldata,
                               browser=browser,
                               rules=(Rule(LinkExtractor(allow=crawl_rules_allow,
                                                         deny=crawl_rules_deny,
                                                         process_value=process_link_value),
                                           callback="parse_obj",
                                           follow=True),))
        reactor.stop()

    crawl()
    # the script will block here until all crawling jobs are finished
    reactor.run()

    log("Closing firefox.")
    browser.quit()

def _get_test_form_inputs(paramname, paramtype):
    from urls import paramname_test_input, paramtype_test_input

    addinputs = []
    if paramtype in paramtype_test_input:
        addinputs += paramtype_test_input[paramtype]

    if paramname in paramname_test_input:
        addinputs += paramname_test_input[paramname]
    
    return addinputs

def _phase2_collate_form_data(url, data):
    collated = {}
    for form in data:
        formsignature = frozenset([form["type"]] +
                                  ["GET:"+x for x in form["params"]["GET"].keys()] +
                                  ["POST:"+x for x in form["params"]["POST"].keys()])

        # convert param values to list on first entry
        if not formsignature in collated:
            formdata = copy.deepcopy(form)
            for param in formdata["params"]["GET"]:
                value = formdata["params"]["GET"][param]["value"]
                addinputs = _get_test_form_inputs(param, formdata["params"]["GET"][param]["type"])
                if value == "":
                    formdata["params"]["GET"][param]["value"] = addinputs
                else:
                    formdata["params"]["GET"][param]["value"] = [value] + addinputs
            for param in formdata["params"]["POST"]:
                value = formdata["params"]["POST"][param]["value"]
                addinputs = _get_test_form_inputs(param, formdata["params"]["POST"][param]["type"])
                if value == "":
                    formdata["params"]["POST"][param]["value"] = addinputs
                else:
                    formdata["params"]["POST"][param]["value"] = [value] + addinputs
            collated[formsignature] = formdata

        # append to value list on subsequent visits
        formdata = collated[formsignature]
        for param in formdata["params"]["GET"]:
            value = form["params"]["GET"][param]["value"]
            values = set(formdata["params"]["GET"][param]["value"])
            if value:
                values.add(value)
            formdata["params"]["GET"][param]["value"] = list(values)
        for param in formdata["params"]["POST"]:
            value = form["params"]["POST"][param]["value"]
            values = set(formdata["params"]["POST"][param]["value"])
            if value:
                values.add(value)
            formdata["params"]["POST"][param]["value"] = list(values)

    return collated.values()

def _phase2_collate_data(phase_data):
    # collate params in data
    output_data = {}
    for url, data in phase_data.items():
        collated_form_data = _phase2_collate_form_data(url, data)
        output_data[url] = collated_form_data
    return output_data

def phase2():
    log_phase(2, "Collating injection points.")

    urlsItems = copy.deepcopy(URLs).items()
    for url, data in urlsItems:
        name = data["name"]
        phase1_data = "output/"+name + "_phase1.json"

        # read phase 1 json
        phase_data = {}
        with open(phase1_data) as json_data:
            phase_data = json.load(json_data)

        # collate phase data
        output_data = _phase2_collate_data(phase_data)

        # write to phase 2 json
        with open("output/"+name + '_phase2.json', 'w') as fp:
            json.dump(output_data, fp, sort_keys=True, indent=4)

def _phase3_confirm_exploit(url, method, param_value_dict):
    exploitable_values = ["del"]
    exploitable_keys = ["pass1", "pass2", "password", "currency", "currency_code"]

    if param_value_dict:
        if any(value in param_value_dict.values() for value in exploitable_values):
            return 1
        if any(key in param_value_dict for key in exploitable_keys):
            return 1
    return 0

def _phase3_output_exploit(url, data_array, o_json_path):
    json_data = {}
    # if the output file exists, read the content of this json file
    if os.path.isfile(o_json_path):
        with open(o_json_path, "r") as json_file:
            if os.stat(o_json_path).st_size > 0:
                json_data = json.load(json_file)
    
    if url in json_data:
        # if url already exists, append the method and parameters
        json_data[url].append(data_array)
    else:
        # if ulr doesn't exist, append the url, method and parameters
        json_data[str(url)] = [data_array]
    
    # create json file
    with open(o_json_path, "w") as outfile:
        json.dump(json_data, outfile, indent=4)

def _phase3_run(json_data, o_json_path):

    _exclude_keys = ["token"]
    _form_num_limit = 100
    _values_num_limit = 100  # set to 2 for app9_admin
    
    urls = json_data.keys()
    for url in urls:
        # url: https://app4.com/user.php
        # if url in _exclude_URLS:
            # continue
        forms = json_data[url]
        print "Form Info: "+form

        rand_forms = []
        if (len(forms) > _form_num_limit):
            print "  " + str(len(forms)) + " forms:" + url
            rand_forms = random.sample(forms, _form_num_limit)
        else:
            rand_forms = forms

        for form in rand_forms:
            # find all combinations for POST
            
            post_param_names = sorted(form["params"]["POST"])
            rand_post_pairs = {}
            for post_param_name in post_param_names:
                values = form["params"]["POST"][post_param_name]["value"]
                print "Values for forms: "+values
                if len(values) > _values_num_limit:
                    print "  length " + str(len(values)) + " : " + post_param_name
                    rand_values = random.sample(values, _values_num_limit)
                    rand_post_pairs[post_param_name] = rand_values
                else:
                    rand_post_pairs[post_param_name] = values
            post_combinations = [dict(zip(post_param_names, prod)) for prod in it.product(*(rand_post_pairs[param_name] for param_name in post_param_names))]
            
            # find all combinations for GET
            get_param_names = sorted(form["params"]["GET"])
            rand_get_pairs = {}
            for get_param_name in get_param_names:
                values = form["params"]["GET"][get_param_name]["value"]
                if len(values) > _values_num_limit:
                    print "  length " + str(len(values)) + " : " + get_param_name
                    rand_get_pairs[get_param_name] = random.sample(values, _values_num_limit)
                else:
                    rand_get_pairs[get_param_name] = values
            get_combinations = [dict(zip(get_param_names, prod)) for prod in it.product(*(rand_get_pairs[param_name] for param_name in get_param_names))]

            print "Get Combination: "+get_combinations
            print "Post Combination: "+post_combinations
            print "Get Comb: "+get_comb
            print "Post Comb"+post_comb

            for get_comb in get_combinations:
                for post_comb in post_combinations:
                    if any(key in get_comb for key in _exclude_keys):
                        continue
                    if any(key in post_comb for key in _exclude_keys):
                        continue

                    arr = []
                    # if post_comb is empty
                    if not post_comb:
                        if not get_comb:
                            continue
                        else:
                            # if post_comb is empty and get_comb is not empty, check for exploit
                            if _phase3_confirm_exploit(url, "GET", get_comb):
                                arr.append({"params": get_comb, "method": "GET"})
                                _phase3_output_exploit(url, arr, o_json_path)
                    # else, if post_comb is not empty
                    else:
                        # if get_comb is empty
                        if not get_comb:
                            if _phase3_confirm_exploit(url, "POST", post_comb):
                                arr.append({"params": post_comb, "method": "POST"})
                                _phase3_output_exploit(url, arr, o_json_path)
                        else:
                            # if both post_comb and get_comb are not empty, check for exploit
                            if _phase3_confirm_exploit(url, "POST", post_comb) or _phase3_confirm_exploit(url, "GET", get_comb):
                                arr.append({"params": post_comb, "method": "POST"})
                                arr.append({"params": get_comb, "method": "GET"})
                                _phase3_output_exploit(url, arr, o_json_path)

def phase3():
    log_phase(3, "Identifying exploitable injection points.")

    urlsItems = copy.deepcopy(URLs).items()
    for url, data in urlsItems:
        name = data["name"]
        # name = "app4_admin"
        phase2_data = "output/"+name + "_phase2.json"

        # read phase 2 json
        if os.path.isfile(phase2_data):
            phase_data = {}
            with open(phase2_data) as json_data:
                phase_data = json.load(json_data)
            
            # delete phase 3 json if exists
            phase3_json_file = "output/"+name + '_phase3.json'
            if os.path.isfile(phase3_json_file):
                os.remove(phase3_json_file)
            
            print "generating " + name + "_phase.json..."
            # collate phase data
            _phase3_run(phase_data, phase3_json_file)

def phase4():
    log_phase(4, "Generating exploit scripts.")


## Crawler
def start_crawl():
    try:
        os.mkdir("output")
    except OSError:
        pass

    try:
        os.mkdir("debug")
    except OSError:
        pass

    # phase1()
    # phase2()
    phase3()
    #phase4()


if __name__=="__main__":
    start_crawl()
