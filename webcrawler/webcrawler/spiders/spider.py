import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
import urlparse
from selenium import webdriver
import time
import re
import os
import unicodedata

# Description of the spider logic
# 1. scan all the href in the start webpage 
# 2. try to find forms within the webpages that we crawl
# 3. if forms are found, we try to login
# 4. Upon login successful, we do something next 
# TODO: I don't think the crawler crawls to all subpages. Need to try and fix this
# TODO: How to not statically define username & password ?
# TODO: How to test the success of the login process (now it is defined statically)?
# TODO: Find the entry point/s of the exploit/s
# TODO: How to reduce/eliminate false positives 


class StackSpider(CrawlSpider):
    name = "stack"
    # crawl within this domain
    allowed_domains = []

    #start url
    start_urls = []

    def __init__(self, category=None, *args, **kwargs):
        super(StackSpider, self).__init__(*args, **kwargs)
        
        self.start_urls = [kwargs.get("urldata")[0]]
        self.allowed_domains = [urlparse.urlparse(self.start_urls[0]).netloc]

        self.need_selenium = False
        self.login_page = None
        self.login_formdata = None
        self.crawl_rules_allow = ()
        self.crawl_rules_deny = ()

        self.login_cookie = None
        urldata = kwargs.get("urldata")[1]
        self.name = urldata.pop("name")

        if urldata:
            try:
                self.need_selenium = urldata.pop("need_selenium")
            except KeyError:
                pass
            try:
                self.login_page = urldata.pop("login_page")
            except KeyError:
                pass
            try:
                self.crawl_rules_allow = urldata.pop("crawl_rules_allow")
                self.crawl_rules_deny = urldata.pop("crawl_rules_deny")
            except KeyError:
                pass

            self.login_formdata = urldata

        self.injection_points = {}

        # clear files
        with open("debug/"+self.name+'_forms.txt', 'w'):
            pass
        with open("debug/"+self.name+'_links.txt', 'w'):
            pass

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    ## Login handling
    def start_requests(self):
        """This function is called before crawling starts."""
        if not self.login_page:
            for u in self.start_urls:
                yield Request(url=u, dont_filter=True)

        if (self.need_selenium):
            login_cookie = self._selenium_login()
            # extract links from response to be crawled, since redirected links get
            # filtered automatically
            links = self.browser.find_elements_by_xpath('//a[@href]')
            links = [l.get_attribute("href") for l in links]
            links = [self._get_full_url(l, self.browser.current_url) for l in links]
            links = [l for l in links if self._is_link_allowed(l)]
            self.start_urls = [self.browser.current_url] + links + self.start_urls

            for u in self.start_urls:
                req = Request(url=u, cookies=login_cookie, dont_filter=True)
                if self.login_cookie is None:
                    self.login_cookie = req.cookies
                yield req
        else:
            yield Request(url=self.login_page, callback=self.login, dont_filter=True)

    def _is_link_allowed(self, link):
        """ Checks if link is allowed to be followed
        """
        denied = [re.match(r, link) for r in self.crawl_rules_deny]
        denied = [x for x in denied if x is not None]

        crawl_rules_allow = self.crawl_rules_allow
        if not self.crawl_rules_allow:
            crawl_rules_allow = (".*",)
            
        allowed = [re.match(r, link) for r in crawl_rules_allow]
        allowed = [x for x in allowed if x is not None]

        return not bool(denied) and bool(allowed)

    def login(self, response):
        """Generate a login request."""
        return [FormRequest.from_response(response,
                                          callback=self.check_login_response, dont_filter=True,
                                          **self.login_formdata)]
                                          
    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        # for debug purposes only -- just to ensure that we are logged
        # in
        isLoggedIn = self.check_login(response)
        if (isLoggedIn == 1):
            self.logger.info("## Login Passed ##")
        else:
            self.logger.info("## Login Failed ##")
        #if "Hi Herman" in response.body:
        self.logger.warning("Successfully logged in. Let's start crawling!")

        # extract links from response to be crawled, since redirected links get
        # filtered automatically
        
        hxs = scrapy.Selector(response)
        links = hxs.xpath('//a/@href').extract()
        links = [self._get_full_url(l, response.url) for l in links]
        links = [l for l in links if self._is_link_allowed(l)]
        self.start_urls = [response.url] + links + self.start_urls 

        return [Request(url=u, dont_filter=True) for u in self.start_urls]

    def _get_full_url(self, link, url):
        """ Returns full url for link
        """
        from webcrawler.settings import process_link_value
        path = urlparse.urljoin(url, link)
        path = process_link_value(path)
        return path

    def _selenium_login(self):
        """ Selenium login
        """
        login_page = self.login_page
        form_xpath = self.login_formdata["formxpath"]
        form_data = self.login_formdata["formdata"]

        self.browser.get(login_page)
        for param, value in form_data.items():
            self.browser.find_element_by_name(param).send_keys(value)
        self.browser.find_element_by_xpath(form_xpath).submit()

        cookies = self.browser.get_cookies()
        # wait for selenium login to finish
        time.sleep(3)
        return cookies
    
    # can add additional checks for possible signs login is successful    
    def check_login(self, response):
        # check if response url contains login. if yes, means not logged in
        if (response.url.find('login') >= 0):
            return 0

        # check if logout string is in the body text
        # if logout is in body text, means already logged in
        bodytext = response.body.lower()
        if (bodytext.find('logout') >= 0 or
            bodytext.find('log out') >= 0):
            return 1

        # check if login strin is in the body text
        # if it is, means the login may have failed
        if (bodytext.find('login') < 0 or
            bodytext.find('log in') < 0):
            return 1
        
        #check if redirected to login page
        if (self.login_page == response.url):
            return 0
        
        # if none matches, just assume it failed       
        return 0

    
    ## Page Parsing
    def parse_start_url(self, response):
        """ parse start urls - Rules are not applied for start urls!!
        http://stackoverflow.com/questions/12736257/why-dont-my-scrapy-crawlspider-rules-work
        """
        self.parse_obj(response)

    def parse_obj(self, response):
        # Scrape data from page
        self.get_all_forms(response)
        self.get_all_links(response)
        return

    def get_all_forms(self, response):
        count = 0
        hxs = scrapy.Selector(response)
        url = response.url

        for form in hxs.xpath("//form"):
            formname = form.xpath("@action").extract()
            if formname:
                formname = self._get_full_url(formname[0], response.url)
            else:
                formname = response.url

            # prune away forms not in domain
            fn = urlparse.urlparse(formname)
            if not fn.netloc == self.allowed_domains[0]:
                continue
                
            formtype = form.xpath("@method").extract()            
            if formtype:
                formtype = formtype[0].upper()
            else:
                formtype = u"GET"

            # collect params
            getparams = {}
            postparams = {}

            # form action url params
            urlparts = urlparse.urlparse(formname)
            formparams = urlparse.parse_qsl(urlparts.query)
            formparams = [(x[0], {"type":u"text",
                                  "value":x[1]},) for x in formparams]
            getparams = dict(formparams)
            
            # Other explicit GET/POST params
            for input in form.xpath(".//input"):
                paramtype = input.xpath("@type").extract()
                if paramtype:
                    paramtype = paramtype[0]
                else:
                    paramtype = u""
                paramvalue = input.xpath("@value").extract()
                if paramvalue:
                    paramvalue = paramvalue[0]
                else:
                    paramvalue = u""
                paramname = input.xpath("@name").extract()

                if paramname:
                    if formtype == "POST":
                        postparams.setdefault(paramname[0], {})
                        postparams[paramname[0]]["type"] = paramtype
                        postparams[paramname[0]]["value"] = paramvalue
                    else:
                        getparams.setdefault(paramname[0], {})
                        getparams[paramname[0]]["type"] = paramtype
                        getparams[paramname[0]]["value"] = paramvalue

            # set dictionary
            # remove params from formname prior to entry
            if getparams or postparams:
                formname = urlparse.urlunparse(list(urlparts)[:3]+["","",""])
                self.injection_points.setdefault(formname, [])
                self.injection_points[formname].append({"type":formtype, "params":{"GET":getparams,
                                                                                   "POST":postparams}})

        forms = hxs.xpath('//form').extract()
        form_fp = open("debug/"+self.name+'_forms.txt', 'a')
        form_fp.write("\n\n### Form in URL:" + response.url + "\n")
        for itr in forms:
            form_fp.write("\n@@@ form number {cnt}\n".format(cnt=count))
            form_fp.write(itr.encode('utf-8').strip())
            count+=1

        form_fp.close()

    def get_all_links(self, response):
        hxs = scrapy.Selector(response)
        links = hxs.xpath('//a/@href').extract()

        for link in links:
            link = self._get_full_url(link, response.url)
            link = urlparse.urlparse(link)

            # prune away links not in domain
            if not link.netloc == self.allowed_domains[0]:
                continue

            # break down into parts
            formname = urlparse.urlunparse(list(link)[:3]+["","",""])
            formtype = u"GET"
            formparams = urlparse.parse_qsl(link.query)
            formparams = [(x[0], {"type":u"text",
                                  "value":x[1]},) for x in formparams]

            if formparams:
                self.injection_points.setdefault(formname, [])
                self.injection_points[formname].append({"type":formtype, "params":{"GET":dict(formparams),
                                                                                   "POST":{}}})

        links_fp = open("debug/"+self.name+'_links.txt', 'a')
        links_fp.write("\n\n### Links in URL:" + response.url + "\n")
        for itr in links:
            if (self.is_ascii(itr)):
                links_fp.write('\n' + itr)
            else:
                links_fp.write('\n' + itr.encode('utf-8'))
                
        links_fp.close()

    def is_ascii(self, str):
        try:
            str.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True


    ## Runs when spider finishes
    def spider_closed(self, spider):
        """ Collate results when spider is done
        """
        if spider is not self:
            return

        # Phase1: write injection points to file
        import json
        with open("output/"+self.name + '_phase1.json', 'w') as fp:
            json.dump(self.injection_points, fp, sort_keys=True, indent=4)
