from scrapy.dupefilter import BaseDupeFilter
import redis
from scrapy.utils.request import request_fingerprint
import scrapy_redis

# 完全自定义
# class DupFilter(BaseDupeFilter):
#     def __init__(self):
#         self.conn = redis.Redis(host='47.104.135.55',port=6379,password='bared@ylMw47GL')
#
#
#
#     def request_seen(self, request):
#         """
#         检测当前请求是否已经被访问过
#         :param request:
#         :return: True表示已经访问过；False表示未访问过
#         """
#         fid = request_fingerprint(request) # 类似MD5的加密
#         result = self.conn.sadd('visited_url',fid)
#         if result == 1:
#             return False
#         return True
#
#         # if request.url in self.visited_url:
#         #     return True
#         # self.visited_url.add(request.url)
#         # return False

# 继承scrapy_redis自定制
from scrapy_redis.dupefilter import RFPDupeFilter
from scrapy_redis.connection import get_redis_from_settings
from scrapy_redis import defaults
class RedisDupFilter(RFPDupeFilter): # 原有基础上扩展让redis键名不用时间戳
    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.

        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.

        Parameters
        ----------
        settings : scrapy.settings.Settings

        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.


        """
        server = get_redis_from_settings(settings)
        # XXX: This creates one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        # TODO: Use SCRAPY_JOB env as default and fallback to timestamp.
        key = defaults.DUPEFILTER_KEY % {'timestamp': 'xiaodongbei'}
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key=key, debug=debug)

"""
settings配置
################################### scrapy_redis连接###############################

REDIS_HOST = '47.104.135.55'                            # 主机名
REDIS_PORT = 6379                                   # 端口

REDIS_PARAMS  = {'password':'bared@ylMw47GL'}                                  # Redis连接参数             默认：REDIS_PARAMS = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True,'encoding': REDIS_ENCODING,}）
# REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient' # 指定连接Redis的Python模块  默认：redis.StrictRedis
REDIS_ENCODING = "utf-8"                            # redis编码类型             默认：'utf-8'

################################ 去重 ###############################
# 四合一 # REDIS_URL = 'redis://user:pass@hostname:9001'       # 连接URL（优先于以上配置）
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'
DUPEFILTER_CLASS = 'ddb.xxx.RedisDupFilter'
"""