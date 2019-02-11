# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup

from meinr.items import MeinrItem


class Meinr1Spider(scrapy.Spider):
    name = 'meinr1'
    # allowed_domains = ['www.baidu.com']
    # start_urls = ['http://m.tupianzj.com/meinv/xiezhen/']
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
    def num(self,url,headers):
        html = requests.get(url=url,headers=headers)
        if html.status_code != 200:
            return '',''
        soup = BeautifulSoup(html.text,'html.parser')
        nums = soup.select('#pageNum li')[3]
        nums = nums.select('a')[0].attrs.get('href')
        num = str(nums[:-5]).split('_')[-1]
        papa = str(nums[:-5]).split('_')[:-1]
        papa = '_'.join(papa)+'_'
        return int(num),papa


    def start_requests(self):
        urls = ['http://m.tupianzj.com/meinv/xiezhen/','http://m.tupianzj.com/meinv/xinggan/','http://m.tupianzj.com/meinv/guzhuang/','http://m.tupianzj.com/meinv/siwa/','http://m.tupianzj.com/meinv/chemo/','http://m.tupianzj.com/meinv/qipao/','http://m.tupianzj.com/meinv/mm/']
        num = 0
        for url in urls:
            num,papa = self.num(url,self.headers)
            for i in range(1,num):
                if i != 1:
                    urlzz = url + papa + str(i) + '.html'
                else:
                    urlzz = url
                yield scrapy.Request(url=urlzz,headers=self.headers,callback=self.parse)
    def parse(self, response):
        # print(response.body)
        htmllist = response.xpath('//div[@class="IndexList"]/ul[@class="IndexListult"]/li')
        # print(htmllist)
        for html in htmllist:
            url = html.xpath('./a/@href').extract()
            title = html.xpath('./a/span[1]/text()').extract()
            # print(url)
            # print(title)
            yield scrapy.Request(url=url[0],meta={
                        'url':url[0],
                        'title':title[0]},
                        headers=self.headers,
                        callback=self.page
             )
    def page(self,response):
        is_it = response.xpath('//div[@class="m-article"]/h1/text()').extract()
        if is_it:
            is_it = is_it[0].strip()
            num = int(is_it[-4])
            a = 0
            for i in range(1,int(num)):
                a += 1
                url = str(response.url)[:-5] + '_' + str(i) + '.html'
                yield scrapy.Request(url=url, headers=self.headers, callback=self.download, meta={
                    'url': response.meta.get('url'),
                    'title': response.meta.get('title'),
                    'num':a

                },dont_filter=True)

    def download(self,response):
        img = response.xpath("//img[@id='bigImg']/@src").extract()
        if img:
            time = MeinrItem()
            time['img'] = img[0]
            time['title'] = response.meta.get('title')
            time['num'] = response.meta.get('num')
            yield time



