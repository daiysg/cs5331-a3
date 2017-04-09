#!/usr/bin/env python
import os
import time
import json
import copy
import urlparse
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

@defer.inlineCallbacks
def crawl(runner, browser):
    from urls import URLs
    from urls import crawl_rules_allow, crawl_rules_deny

    urlsItems = copy.deepcopy(URLs).items()
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

## Phase functions
def phase1():
    log_phase(1, "Crawling sites from urls.py for injection points.")

    log("Launching firefox for selenium.")
    browser = webdriver.Firefox()
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
    crawl(runner, browser)
    # the script will block here until all crawling jobs are finished
    reactor.run()

    log("Closing firefox.")
    browser.quit()
