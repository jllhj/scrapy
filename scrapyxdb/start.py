import sys
from scrapy.cmdline import execute

if __name__ == '__main__':
    # execute(["scrapy","crawl","chouti","--nolog"]) #单个爬虫
    execute(["scrapy", "crawlall", "--nolog"])