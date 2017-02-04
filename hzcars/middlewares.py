# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy import signals
from selenium.webdriver.support.ui import WebDriverWait
import logging, traceback


class PhantomJSMiddleware(object):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            PHANTOMJS_PATH = kwargs["PHANTOMJS_PATH"]
            self.driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, service_args=["--ssl-protocol=any", "--ignore-ssl-errors=true", "--load-images=false", "--disk-cache=true"])
        except Exception as e:
            self.logger.error(e, exc_info=True)
            exit(-2)

    def process_request(self, request, spider):
        if request.meta.has_key("parse") and request.meta['parse'] is True:
            self.logger.info("Get url %s \n", request.url)
            self.driver.get(request.url)
            try:
                WebDriverWait(self.driver, 10).until(lambda x:self.driver.execute_script("return document.readyState") == "complete")
            except Exception as e:
                self.logger.warning(traceback.print_exc())
            content = self.driver.page_source.encode('utf-8')
            url = self.driver.current_url.encode('utf-8')
            if content == "<html><head></head><body></body></html>":
                self.logger.warning("Failed to get response from url %s \n", request.url)
                return None
            else:
                return HtmlResponse(url, encoding = 'utf-8', status = 200, body = content)
        else:
            return None

    @classmethod
    def from_crawler(cls, crawler):
        kwargs = {"PHANTOMJS_PATH": crawler.settings["PHANTOMJS_PATH"]}
        o = cls(**kwargs)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider, reason):
        self.logger.info("Webdriver Quit")
        self.driver.quit()
