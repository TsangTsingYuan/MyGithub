import requests
from bs4 import BeautifulSoup
import traceback
import re
from Database import db

def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''

def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, 'GB2312')
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')

    for i in a:
        try:
            href = i.attrs['href']
            stockCode = re.findall(r"[s][hz]_\d{6}", href)[0].replace('_', '')
            lst.append(stockCode)

            #print(lst)
        except:
            continue

def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock + '.html'
        html = getHTMLText(url)
        try:
            if html == '':
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class':'stock-info'})

            name = stockInfo.find_all(attrs={'class':'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})

            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            # 使用infoDict集合
            collection = db.infoDict
            collection.insert(infoDict)  # 添加数据
            collection.save(infoDict)  # 添加数据
            count = count + 1
            print('\r当前进度：{:.2f}%'.format(count * 100 / len(lst)), end='')
        except:
            traceback.print_exc()
            #count = count + 1
            #print('\r当前进度：{:.2f}%'.format(count * 100 / len(lst)), end='')
            continue
    print('存入数据库操作完成')

def getStockInfo2(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock + '/nc.shtml'
        html = getHTMLText(url)
        try:
            if html == '':
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parse')

            name = soup.find(attrs={'id':'stockName'})
            infoDict.update({'股票名称': name.text.split()[0]})

            keyList = soup.find_all('th')
            valueList = soup.find_all('td')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print('\r当前进度：{:.2f}%'.format(count*100/len(lst)),end='')
        except:
            #traceback.print_exc()
            count = count + 1
            print('\r当前进度：{:.2f}%'.format(count * 100 / len(lst)), end='')
            continue

def main():
    stock_list_url = 'http://quote.stockstar.com/stock/stock_index.htm'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    stock_info_url2 = 'http://finance.sina.com.cn/realstock/company/'
    output_file = 'F:\pythonPRJ\StockInfo1.txt'
    output_file2 = 'F:\pythonPRJ\StockInfo2.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)
    #getStockInfo2(slist, stock_info_url2, output_file2)

main()
