import requests
import re
import traceback
from Database import db2

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def parsePage(ilt, html):
    try:
        plt = re.findall(r'"price":"[\d\.]*"', html)
        tlt = re.findall(r'"title":".*?"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])

    except:
        print('')

'''
def printGoodsList(ilt):
    tplt = '{:4}\t{:8}\t{:16}'
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))
'''
def storeGoodsList(ilt):
    #print(ilt)
    GoodsDict = {}
    count = 0
    for g in ilt:
        count = count + 1
        try:
            GoodsDict["_id"] = count    #手动添加id值,当插入的数据带有_id的字段时,mongodb就不再自动生成id
            GoodsDict["价格"] = g[0]
            GoodsDict["商品名称"] = g[1]
            collection = db2.GoodsDict
            collection.insert(GoodsDict)  # 添加数据
            collection.save(GoodsDict)  # 添加数据 无则加之，有则改之（更新数据）
        except:
            #traceback.print_exc()
            continue




def main():
    goods = '鼠标'
    depth = 2
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(48*i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    #printGoodsList(infoList)
    storeGoodsList(infoList)

main()
