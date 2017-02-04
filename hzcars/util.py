# -*- coding: utf-8 -*-

"""
  Author: FangPengdong
  Date: 2017/1/10 15:28
  Description:
  
"""
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst

def strip(value):
    if type(value) == str or type(value) == unicode:
        return value.strip()
    else:
        return value

class HzcarsLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(strip)