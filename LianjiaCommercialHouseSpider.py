from scrapy import Request
from scrapy.spiders import Spider
from Amap.items import LianjiaCommercialHouseItem
import pymysql,scrapy,re,time

class LianjiaCommercialHouse(Spider):
    name = 'LianjiaCommercialHouse'
    allowed_domains = ['gz.lianjia.com']
    # districts = ['越秀区', '白云区', '天河区', '海珠区', '荔湾区', '番禺区', '花都区', '增城区', '黄浦区',    '从化区', '南沙区']
    # #               0         1         2           3          4          5         6           7           8            9         10
    # pinyin =  ['yuexiu', 'baiyun', 'tianhe', 'haizhu', 'liwan', 'panyu', 'huadu', 'zengcheng', 'huangpu', 'conghua','nansha']
    districts_index = 0
    url = 'https://gz.lianjia.com/ershoufang/rs{0}/'
    start_urls = [url]

    # 连接数据库studentscore中麦当劳信息的数据表amapcommercialhouseitem
    def __init__(self):
        self.conn = pymysql.connect(
            host = 'localhost',
            db = 'studentscore',
            user = 'root',
            passwd = '123456',
            charset = 'utf8',
            use_unicode = True
        )
        self.cursor = self.conn.cursor()
        # sql = 'SELECT id,name FROM amapcommercialhouseitem where price IS NULL'
        # sql = 'SELECT id,name FROM amapcommercialhouseitem WHERE id>42525 AND price IS NULL'
        sql = 'SELECT id,name FROM amapcommercialhouseitem WHERE id<30000 AND id>10000 AND price IS NULL'
        self.cursor.execute(sql)
        self.prices = self.cursor.fetchall()  # prices是从"amapcommercialhouseitem"读取到的信息
        self.cursor.close()
        self.conn.close()

    # 该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request
    # def start_requests(self):
    #     self.districts_index = 0
    #     temp = self.prices[0]  # prices是从"amapcommercialhouseitem"读取到的信息
    #     for d in self.districts: #用于判断该行的小区属于哪个区
    #         if (d in temp[2]):
    #             print('start_requests:  ', temp[1], '  ', temp[2])
    #             request = scrapy.Request(
    #                 self.url.format(self.pinyin[self.districts_index], temp[1]),
    #                 dont_filter=True,
    #                 callback=self.parse
    #             )
    #             yield request
    #         self.districts_index += 1


    def parse(self, response):
        for temp in self.prices:
            print('id:  ', temp[0], '   name: ', temp[1])
            request = scrapy.Request(
                self.url.format(temp[1]),
                dont_filter=True,
                callback=self.parsePrice
            )
            request.meta['CommercialHouse'] = temp
            yield request
            time.sleep(0.5)
            # 命令行调试代码，需要调试时把下面两行的代码注释去掉
            # from scrapy.shell import inspect_response
            # inspect_response(response, self)


    def parsePrice(self,response):
        # 命令行调试代码，需要调试时把下面两行的代码注释去掉
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        CommercialHouse = response.meta['CommercialHouse']
        item = LianjiaCommercialHouseItem()
        item['CommercialHouseId'] = CommercialHouse[0]
        name = CommercialHouse[1]
        numbers_str = response.xpath('//div[@class="leftContent"]/div[@class="resultDes clear"]/h2/span/text()').extract_first() #共找到 X 套广州二手房
        number = int(numbers_str)
        print('is number int? --> ', isinstance(number, int), '   number:',number )
        if (number!=0):
            price_sentence = response.xpath('//ul/li[1]/div[@class="info clear"]/div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').extract_first()
            #price_sentence是单价XXXXX元/平米，还需要正则表达式进行提取数字
            str(price_sentence)
            print( 'id:', CommercialHouse[0],  '  name:',  name,'    price_sentence: ',price_sentence )
            item['CommercialHousePrice'] = re.findall("\d+",price_sentence)[0]
            yield item


