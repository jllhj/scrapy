from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
"""
在spiders同级创建任意目录，如：commands
在其中创建 crawlall.py 文件 （此处文件名就是自定义的命令）
在settings.py 中添加配置 COMMANDS_MODULE = '项目名称.目录名称'
在项目目录执行命令：scrapy crawlall 
"""


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self): # 用 --help 增加了提示信息
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()
        print(spider_list) # 找到所有的爬虫
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()