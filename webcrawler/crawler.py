#!/usr/bin/env python
import os
import time
import json
import copy

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
from phase3 import phase3

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
    phase3("outputpath/")
    #phase4()


if __name__=="__main__":
    start_crawl()
