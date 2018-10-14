# -*- coding: utf-8 -*-
import scrapy
import re
import requests

class StockSpider(scrapy.Spider):
    name = 'stock'
    #allowed_domains = ['baidu.com']
    start_urls = ['http://quote.stockstar.com/stock/stock_index.htm']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stockCode = re.findall(r"[s][hz]_\d{6}", href)[0].replace('_', '')
                url = 'https://gupiao.baidu.com/stock/' + stockCode + '.html'
                if response.status != 200:  #判断网页响应更换代理IP
                    requests.meta["change_proxy"] = True

                yield scrapy.Request(url, callback=self.parse_stock)
            except:
                continue

    def parse_stock(self, response):
        infoDict = {}
        stockInfo = response.css('.stock-info')
        name = stockInfo.css('.bets-name').extract()[0]
        keyList = stockInfo.css('dt').extract()
        valueList = stockInfo.css('dd').extract()

        for i in range(len(keyList)):
            key = re.findall(r'>.*</dt>', keyList[i])[0][1:-5]
            try:
                val = re.findall(r'\d+\.?.*</dd>', valueList[i])[0][0:-5]
            except:
                val = '--'
            infoDict[key] = val

        infoDict.update(
            {'股票名称': re.findall('\s.*\(', name)[0].split()[0] + \
             re.findall('\>.*\<', name)[0][1:-1]}
        )
        yield infoDict





