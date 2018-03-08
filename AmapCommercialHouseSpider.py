from scrapy import Request
from scrapy.spiders import Spider
from Amap.items import AmapCommercialHouseItem
import pymysql,scrapy,json

class AmapCommercialHouse(Spider):
    name = 'AmapCommercialHouse'
    allowed_domains = ['restapi.amap.com']
    key = '85692e965f1085a96d17e27ac6486979' # 高德地图Web服务的key
    radius = 1000 # 以麦当劳的经纬度为中心的半径
    url = 'http://restapi.amap.com/v3/place/around?key={0}&location={1}&types=120300&radius={2}&extensions=all&page={3}&offset=15'
    start_urls = [url]
    # uid = 1

    # 连接数据库studentscore中麦当劳信息的数据表allmacdonalditem
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            db='studentscore',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()
        sql = 'select id,location from allmacdonalditem'
        self.cursor.execute(sql)
        self.macdonalds = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()

    def parse(self, response):
        # item = AmapCommercialHouseItem()
        for temp in self.macdonalds:
            request = scrapy.Request(
                self.url.format(self.key, temp[1], self.radius, 0),
                dont_filter=True,
                callback=self.parseCommercialHouse
            )
            request.meta['macdonald'] = temp # 将当前行的麦当劳分店的id和location通过meta属性传递到下一个
            request.meta['index'] = 0  # 页数
            yield request


    def parseCommercialHouse(self, response):
        result = json.loads(response.body)
        resultList = result.get('pois', '')  # pois是一个数组，里面每个元素表示一个小区
        macdonald = response.meta['macdonald'] #正在遍历的麦当劳分店的id和经纬度
        if '' != resultList and len(resultList) > 0:
            for result in resultList:
                item = AmapCommercialHouseItem()
                # item['id'] = self.uid          # 容易造成并发错误
                # self.uid += 1
                item['McdonaldsId'] = macdonald[0]  # 1
                item['CommercialHouseName'] = result['name']  # 2
                item['CommercialHouseLocation'] = result['location']  # 3
                # item['CommercialHouseAddress'] = result['address']    # 4
                if not result['address']:
                    item['CommercialHouseAddress'] = ''
                else:
                    item['CommercialHouseAddress'] = result['adname'] + result['address']
                item['CommercialHouseAdcode'] = result['adcode']      # 5
                item['CommercialHouseDistance'] = result['distance']  # 6
                item['CommercialHouseTypecode'] = result['typecode']  # 7
                self.check(item)
                yield item
            index = response.meta['index'] + 1
            request = scrapy.Request(
                self.url.format(self.key, macdonald[1],self.radius, index),
                dont_filter=True,
                callback=self.parseCommercialHouse
            )
            request.meta['macdonald'] = macdonald
            request.meta['index'] = index
            yield request

    def check(self, item):
        for key, val in item.items():
            if not val:
                item[key] = None
