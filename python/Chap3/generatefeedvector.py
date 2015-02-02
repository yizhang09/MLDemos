# coding:utf-8
__author__ = 'zhangyi'

import feedparser
import re


#获取rss feed 单词计数
def getwordcounts(url):
    try:
        d = feedparser.parse(url)
    except EOFError:
        print(url + ' error')

    wc = {}

    if d.entries == {}:
        return

    for e in d.entries:
        if 'summery' in e:
            summery = e.summery
        else:
            summery = e.description

        words = getwords(e.title + '' + summery)
        #单词计数
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return d.feed.title, wc


#清理html标签 返回文字
def getwords(html):
    txt = re.compile(r'<[^>]+>').sub("", html)

    #获取单词
    words = re.compile(r'[^A-Z^a-z]').split(txt)

    return [word.lower() for word in words if word != '']


apcount = {}
wordcounts = {}

for feedurl in file('feedlist.txt'):
    try:
        print(feedurl)
        title, wc = getwordcounts(feedurl)
        print(title)
    except Exception:
        continue
    wordcounts[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1

#for w in getwordcounts('http://feeds.bbci.co.uk/news/rss.xml'):
#    print(w)



