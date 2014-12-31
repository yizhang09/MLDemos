__author__ = 'zhangyi'

from searchengine import searchengine

pagelist = ['http://www.infoq.com/cn']
crawler = searchengine.crawler('')
crawler.crawl(pagelist)