# -*- coding: utf-8 -*-
import sys,datetime
import os

from meinr.spiders.meinr1 import Meinr1Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())
process.crawl(Meinr1Spider)
process.start()