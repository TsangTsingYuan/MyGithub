# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from MySchool.items import MyschoolItem
import json

from urllib.parse import urljoin


class SchoolSpider(scrapy.Spider):
    name = 'school2'
    allowed_domains = ['gkcx.eol.cn']
    # 三年专业录取线请求地址,数据通过ajax更新填充表格
    #实际请求URL如下，可根据要请求的信息单独构造URL
    #注意分析网页时要把messtype=jsonp改为messtype=json,否则json.loads报错
    '''
   https://data-gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=json\
    &provinceforschool=&schooltype=&page=2&size=10&keyWord=&schoolproperty=\
    &schoolflag=&province=&fstype=&zhaoshengpici=&fsyear=&zytype= 
    '''
    start_urls = ['https://data-gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=json&fsyear=2017&pagesize=10',
                 #'https://data-gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=json&fsyear=2016&pagesize=10',
                 #'https://data-gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=json&fsyear=2015&pagesize=10',
                  ]

    '''
    def parse(self, response):
        school = MyschoolItem()
        #数据以json格式提供，详见querySpecialtyScore.json
        result = json.loads(response.body)
        schooldata = result['school']   #得到一个列表
        for filed in school.fields:
            for daxue in schooldata:    #得到字典
                school[filed] = daxue.get(filed)
        yield school
    '''

    def parse(self, response):
        # 数据以json格式提供，详见querySpecialtyScore.json
        #print(eval(response.body)) #得到一个字典
        result = eval(response.body)

        #求页数
        record =result['totalRecord']   #得到一个字典record
        r = int(record['num']) // 10
        #print(r,int(record['num']))
        #print(response.url)
        query_url = response.url
        if int(record['num']) % 10 != 0:
            r +=1
        for page in range(1, r+1):
            url = '&page=' + str(page)
            #print(query_url + url)
            yield Request(query_url + url, callback=self.parse_item, dont_filter=True)
        #print(query_url + url)
        #爬取学校数据

    def parse_item(self, response):

        result = eval(response.body)
        #result = json.loads(response.body)
        schooldata = result['school']  # 得到一个列表schooldata
        #print(schooldata)

        for daxue in schooldata:
            #print('********')
            #school['localprovince'] = [daxue.get('localprovince')]
            #print(school['localprovince'])
            school = MyschoolItem()     #放在for循环内，否则yield会重复提交,每一次循环是新的item,yield不要放在双层循环内
            school['schoolname'] = [daxue.get('schoolname')]  # 如果要数据上传到appery.io要加[],否则appery.io只会存储首个字符
            school['specialtyname'] = [daxue.get('specialtyname')]
            school['localprovince'] = [daxue.get('localprovince')]
            school['studenttype'] = [daxue.get('studenttype')]
            school['year'] = [daxue.get('year')]
            school['batch'] = [daxue.get('batch')]
            school['var_score'] = [daxue.get('var_score')]
            school['max'] = [daxue.get('max')]
            school['min'] = [daxue.get('min')]
            #print(school)
            yield school
