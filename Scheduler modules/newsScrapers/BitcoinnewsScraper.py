# -*- coding: utf-8 -\*-
"""
Created on Sat Jan 18 11:25:59 2020
Crawl bitcoin news from newsBTC.com
@author: Novin
"""
import json
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
from SentimentAnalysis. predictionModule import predict


def loadPage(url, fileName=None):
    # url of rss feed
    try:
        # creating HTTP response object from given url
        resp = requests.get(url, timeout=3)
        fail = 'fail'
        if resp.status_code == 200:
            # saving the xml file
            with open(fileName, 'wb') as f:
                f.write(resp.content)
                f.close()
                return 1
        else:
            with open(fileName, 'wb') as f:
                f.write(fail)
                f.close()

                return -1

        resp.close()
        resp.raise_for_status()

    except requests.exceptions.HTTPError as htError:
        print('Http Error: ', htError)

    except requests.exceptions.ConnectionError as coError:
        print('Connection Error: ', coError)
    except requests.exceptions.Timeout as timeOutError:
        print('TimeOut Error: ', timeOutError)
    except requests.exceptions.RequestException as ReError:
        print('Something was wrong: ', ReError)
    return (-1)


def parseXML(xmlfile):
    try:

        tree = ET.parse(xmlfile)
        # get root element
        root = tree.getroot()
        # create empty list for news items
        newsitems = []
        # iterate news items
        for item in root:
            for item in item.findall('item'):
                news = {}
                category = {}
                for child in item:

                    if child.tag == '{http://purl.org/rss/1.0/modules/content/}encoded':
                        news['encoded'] = child.text
                    elif child.tag == '{http://wellformedweb.org/CommentAPI/}commentRss':
                        news['commentRss'] = child.text
                    elif child.tag == '{http://purl.org/rss/1.0/modules/slash/}comments':
                        news['comments'] = child.text
                    elif child.tag == '{com-wordpress:feed-additions:1}post-id':
                        news['post-id'] = child.text
                    elif child.tag == '{http://purl.org/dc/elements/1.1/}creator':
                        news['creator'] = child.text
                    elif child.tag == 'category':
                        category['item{}'.format(len(category) + 1)] = child.text
                    elif len(child.attrib) > 2:
                        news['thImage'] = child.attrib['url']

                    else:
                        news[child.tag] = child.text

                    news['category'] = category
                newsitems.append(news)
        return newsitems
    except:
        print("Parse XML Error!")




def JsonItemStandard(newsItem):
    # title : News Headline
    # articleBody : News content
    # pubDate : news timestamp
    # keywords : news keywords
    # author : author of news
    # url : url
    # summary : Breif summary about news
    # provider : news provider
    try:

        CryptoOtions = {'btcusd', 'bitcoin', 'cryptocurrency',
                        'ethusd', 'etherium', 'crypto', 'xpr',
                        'ripple', 'altcoin', 'crypto'}
        CommoditiesOptions = {'oil', 'gold', 'silver', 'wti', ',brent', 'commodities', 'xauusd', 'metals'}
        item = {}
        item['title'] = newsItem['title']
        item['articleBody'] = newsItem['description']
        currentDate = datetime.strptime(newsItem['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
        # currentDateString = currentDate.strftime('%a, %d %b %Y %H:%M:%S Z')

        item['pubDate'] = int(currentDate.timestamp())
        keywords = [w.lower() for w in newsItem['category'].values()]
        # item['keywords'] = list(newsItem['category'].values())
        item['keywords'] = keywords
        item['author'] = newsItem['creator']
        item['link'] = newsItem['link']
        item['provider'] = 'NewsBTC'

        item['summary'] = ''
        #item['sentiment'], item['sentimentScore'], item['vector'] = predict(item)
        item['thImage'] = newsItem['thImage']
        item['images'] = ''
        if list(filter(lambda x: x.lower() in str(newsItem['category']), CryptoOtions)):
            item['category'] = 'Cryptocurrency'
        elif list(filter(lambda x: x.lower() in str(newsItem['category']), CommoditiesOptions)):
            item['category'] = 'Commodities'
        else:
            item['category'] = 'Forex'
        return item
    except:
        print("Error in standardization!")



def checkForExist1(query):
    url = 'http://localhost:5000/Robonews/v1/news'
    resp = requests.get(url, params=query)
    resp = json.loads(resp.text)
    return resp['data']


def saveInMongo1(newsItem):
    for item in newsItem:
        querry = {'link': str(item['link'])}
        # mydoc = mycol.find(querry)
        exist = checkForExist1(querry)
        if not exist:
            item = JsonItemStandard(item)
            url = 'http://localhost:5000/Robonews/v1/news'
            resp = requests.post(url, json=item)
            print(resp.text)

    print('+---------------------------------------------+')




def bitcoinNewsScrapper():
    try:

        url = 'https://www.newsbtc.com/feed/'
        filename = 'topBTCnewsfeed.xml'
        # load RSS File From Url
        now = datetime.now()
        print('Crawling of bitcoin news Startedat ' + now.strftime('%a, %d %b %Y %H:%M:%S Z') + '!!')
        print('+---------------------------------------------+')
        code = loadPage(url, filename)
        if code == 1:
            # parse xmlzz file
            newsitems = parseXML(filename)
            # store news items in a csv file
            saveInMongo1(newsitems)
    except:
        print("Unregular Error!")



def main():
   bitcoinNewsScrapper()

if __name__ == "__main__":

    # calling mpai2n function 
    main()

