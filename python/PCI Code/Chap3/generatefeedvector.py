# coding:utf-8
__author__ = 'zhangyi'

import feedparser
import re


# 获取rss feed 单词计数
def getwordcounts(url):
    try:
        d = feedparser.parse(url)
    except EOFError:
        print(url + ' error')

    wc = {}

    print(len(d.entries))

    if len(d.entries) == 0:
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


#全局单词计数
apcount = {}
#每个feedurl对应的单词计数
wordcounts = {}

feedlist = [line for line in file('feedlist.txt')]

for feedurl in file('feedlist.txt'):
    try:
        print(feedurl)
        title, wc = getwordcounts(feedurl)
        if(title == ''):
            continue
        print(title+'\n')
    except Exception:
        continue
    wordcounts[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1

wordlist = []
for w, bc in apcount.items():
    frac = float(bc) / len(feedlist)
    if (frac > 0.1 and frac < 0.5):
        wordlist.append(w)

out = file("blogdata.txt", "w")
out.write("Blog")
for word in wordlist: out.write('\t%s', word)
out.write('\n')
for blog, wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % word)
        else:
            out.write('\t0')
    out.write('\n')

#for w in getwordcounts('http://feeds.bbci.co.uk/news/rss.xml'):
#    print(w)



