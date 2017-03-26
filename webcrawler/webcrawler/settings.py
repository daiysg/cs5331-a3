# -*- coding: utf-8 -*-

# Scrapy settings for webcrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'webcrawler'

SPIDER_MODULES = ['webcrawler.spiders']
NEWSPIDER_MODULE = 'webcrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webcrawler (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'webcrawler.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'webcrawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'webcrawler.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

AJAXCRAWL_ENABLED = True

# Handling duplicates
# import os
# from scrapy.dupefilters import RFPDupeFilter
# from scrapy.utils.request import request_fingerprint

# class CustomFilter(RFPDupeFilter):
#     """A dupe filter that considers specific ids in the url"""
#     def __getid(self, request):
#         #mm = url.split("&refer")[0] #or something like that
#         params = request.meta.copy()
#         try:
#             params.pop("depth")
#         except KeyError:
#             pass
        
#         mm = "{0},{1}".format(request.url, str(params))
#         return mm

#     def request_seen(self, request):
#         fp = self.__getid(request)
#         if fp in self.fingerprints:
#             return True
#         self.fingerprints.add(fp)
#         if self.file:
#             self.file.write(fp + os.linesep)

#DUPEFILTER_CLASS = 'webcrawler.settings.CustomFilter'
#DUPEFILTER_DEBUG = True

#DEPTH_LIMIT = 3
#DEPTH_STATS = False

import urlparse

def process_link_value(link):
    """ Fix bad links from link extractor
    """
    linkp = urlparse.urlparse(link)
    # means bad url: https://app8.com/app8.com/upload/...
    if linkp.path.startswith("/"+linkp.netloc):
        linkp = list(linkp)
        linkp[2] = linkp[2].replace("/"+linkp[1], "", 1)
        link = urlparse.urlunparse(linkp)
    return link


from scrapy.downloadermiddlewares.redirect import RedirectMiddleware, MetaRefreshMiddleware
from six.moves.urllib.parse import urljoin
from scrapy.utils.response import get_meta_refresh
from scrapy.http import HtmlResponse

class CustomRedirectMiddleware(RedirectMiddleware):
    """Handle redirection of requests based on response status and meta-refresh html tag"""

    def process_response(self, request, response, spider):
        if request.meta.get('dont_redirect', False):
            return response

        if request.method == 'HEAD':
            if response.status in [301, 302, 303, 307] and 'Location' in response.headers:
                redirected_url = urljoin(request.url, response.headers['location'])
                redirected_url = process_link_value(redirected_url)
                redirected = request.replace(url=redirected_url)
                return self._redirect(redirected, request, spider, response.status)
            else:
                return response

        if response.status in [302, 303] and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected_url = process_link_value(redirected_url)
            redirected = self._redirect_request_using_get(request, redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        if response.status in [301, 307] and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected_url = process_link_value(redirected_url)
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        return response

class CustomMetaRefreshMiddleware(MetaRefreshMiddleware):

    enabled_setting = 'METAREFRESH_ENABLED'

    def __init__(self, settings):
        super(MetaRefreshMiddleware, self).__init__(settings)
        self._maxdelay = settings.getint('REDIRECT_MAX_METAREFRESH_DELAY',
                                         settings.getint('METAREFRESH_MAXDELAY'))

    def process_response(self, request, response, spider):
        if request.meta.get('dont_redirect', False) or request.method == 'HEAD' or \
                not isinstance(response, HtmlResponse):
            return response

        if isinstance(response, HtmlResponse):
            interval, url = get_meta_refresh(response)
            if url and interval < self._maxdelay:
                url = process_link_value(url)
                redirected = self._redirect_request_using_get(request, url)
                return self._redirect(redirected, request, spider, 'meta refresh')

        return response

DOWNLOADER_MIDDLEWARES = {
    'webcrawler.settings.CustomMetaRefreshMiddleware': 580,
    'webcrawler.settings.CustomRedirectMiddleware': 600,
    'scrapy.downloadermiddleware.redirect.RedirectMiddleware': None,
    'scrapy.downloadermiddleware.redirect.MetaRefreshMiddleware': None,
}


CLOSESPIDER_TIMEOUT = 300
