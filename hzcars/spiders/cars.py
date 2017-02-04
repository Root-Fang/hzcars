# -*- coding: utf-8 -*-
import scrapy, re, urlparse, unicodedata
from scrapy import Request
from scrapy.loader.processors import MapCompose
from datetime import datetime
from w3lib.html import remove_tags
from hzcars.util import HzcarsLoader
from hzcars.items import CompetitionItem, LotteryItem
from hzcars.db.modules import CompetitionResult, LotteryResult



class CarsSpider(scrapy.Spider):
    name = "cars"
    allowed_domains = ["xkctk.hzcb.gov.cn"]
    start_urls = ['http://xkctk.hzcb.gov.cn/gbl/']

    def start_requests(self):
        for url in self.__class__.start_urls:
            req = Request(url=url, callback=self.parse)
            yield req

    def parse(self, response):
        self.logger.info("Start to parse the url %s \n", response.url)
        lst = response.css("td.align_ceter a")
        for lnk in lst:
            href = lnk.css("::attr(href)")
            if len(href)>0:
                href = href.extract()[0]
                title = lnk.css("::text").extract()[0]
                try:
                    re.compile(u"\d{4}年\d{1,2}月杭州市小客车增量指标竞价情况").match(title).group()
                except Exception as e:
                    try:
                        re.compile(u"\d{4}年\d{1,2}月杭州市小客车增量指标摇号结果公告").match(title).group()
                    except Exception as e:
                        pass
                    else:
                        yield Request(url=href, callback=self.parse_lottery_item)
                else:
                    yield Request(url=href, callback=self.parse_competition_item)
            else:
                continue

        nextpage = response.css("li.next>a")

        if len(nextpage)>0:
            lnk = nextpage.css("::attr(href)").extract()[0]
            yield Request(url=lnk, callback=self.parse)

    def parse_competition_item(self, response):
        data = {}
        article = "".join(MapCompose(remove_tags)(response.css("div.details p").extract()))
        article = unicodedata.normalize("NFKD", article).replace(" ", "")
        try:
            personal_total = re.compile(u"个人增量指标(\d+)个").search(article).group(1)

        except Exception as e:
            pass
        else:
            data['personal_total'] = personal_total

        try:
            corporate_total = re.compile(u"单位增量指标(\d+)个").search(article).group(1)

        except Exception as e:
            pass
        else:
            data['corporate_total'] = corporate_total

        try:
            personal_participate_total, corporate_participate_total = re.compile(u"有效编码数个人为(\d+)个.?单位为(\d+)个")\
                .search(article).group(1,2)
        except Exception as e:
            pass
        else:
            data['personal_participate_total'] = personal_participate_total
            data['corporate_participate_total'] = corporate_participate_total

        try:
            personal_min_price, corporate_min_price = re.compile(u"最低成交价为个人(\d+)元.?单位(\d+)元")\
                .search(article).group(1,2)
        except Exception as e:
            pass
        else:
            data['personal_min_price'] = personal_min_price
            data['corporate_min_price'] = corporate_min_price

        try:
            personal_min_price_total, personal_min_price_volume = re.compile(u"个人最低成交价的报价人数为(\d+)人.?成交(\d+)人")\
                .search(article).group(1,2)
        except Exception as e:
            pass
        else:
            data['personal_min_price_total'] = personal_min_price_total
            data['personal_min_price_volume'] = personal_min_price_volume

        try:
            corporate_min_price_total, corporate_min_price_volume = re.compile(u"单位最低成交价的报价个数为(\d+)个.?成交(\d+)个")\
                .search(article).group(1,2)
        except Exception as e:
            pass
        else:
            data['corporate_min_price_total'] = corporate_min_price_total
            data['corporate_min_price_volume'] = corporate_min_price_volume

        try:
            personal_avg_price, corporate_avg_price = re.compile(u"平均成交价为个人(\d+)元.?单位(\d+)元")\
                .search(article).group(1,2)
        except Exception as e:
            pass
        else:
            data['personal_avg_price'] = personal_avg_price
            data['corporate_avg_price'] = corporate_avg_price

        try:
            year, month = re.compile(u"(\d{4})年(\d{1,2})月").search(article).group(1,2)
        except Exception as e:
            pass
        else:
            month = "{0}-{1}".format(year, month)
            data['month'] = datetime.strptime(month, "%Y-%m").strftime("%Y-%m")

        data['table'] = CompetitionResult

        yield self.insert_item(response, CompetitionItem, **data)

    def parse_lottery_item(self, response):
        data = {}
        article = "".join(MapCompose(remove_tags)(response.css("div.details p").extract()))
        article = unicodedata.normalize("NFKD", article).replace(" ", "")

        try:
            personal_total, corporate_total = re.compile(u"个人指标(\d+)个.?单位指标(\d+)")\
                .search(article).group(1,2)
        except Exception as e:
            pass
        else:
            data['personal_total'] = personal_total
            data['corporate_total'] = corporate_total

        try:
            personal_participate_total, corporate_participate_total = re.compile(u"个人有效编码数(\d+)个.?单位有效编码数(\d+)个")\
                .search(article).group(1,2)
        except Exception as e:
            pass
        else:
            data['personal_participate_total'] = personal_participate_total
            data['corporate_participate_total'] = corporate_participate_total

        try:
            year, month = re.compile(u"(\d{4})年(\d{1,2})月").search(article).group(1,2)
        except Exception as e:
            pass
        else:
            month = "{0}-{1}".format(year, month)
            data['month'] = datetime.strptime(month, "%Y-%m").strftime("%Y-%m")

        data['table'] = LotteryResult

        yield self.insert_item(response, LotteryItem, **data)

    def insert_item(self, response, module, **kwargs):
        load = HzcarsLoader(item=module(), response=response)
        for key, val in kwargs.items():
            if module.fields.has_key(key):
                load.add_value(key, val)
        return load.load_item()