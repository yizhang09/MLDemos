__author__ = 'zhangyi'

from searchengine import searchengine

pagelist = ['http://www.cnblogs.com/']
crawler = searchengine.crawler('')
crawler.crawl(pagelist)

