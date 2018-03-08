# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs,pymysql,json,traceback
from Amap.items import CommercialHouseItem,AmapCommercialHouseItem,LianjiaCommercialHouseItem

class AmapPipeline(object):
    def process_item(self, item, spider):
        return item

#从高德地图爬取得到的
class CommercialHosePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            db='studentscore',
            user='root',  # replace with you user name
            passwd='123456',  # replace with you password
            charset='utf8',
            use_unicode=True,
        )

    def process_item(self, item, spider):
        self.conn.ping(True)  # Check if the server is alive
        try:
            cursor = self.conn.cursor()

            if isinstance(item, LianjiaCommercialHouseItem): # 参数1:实例对象 c参数2:可以是直接或间接类名、基本类型或者由它们组成的元组  返回:如果对象的类型与参数二的类型相同则返回 True，否则返回 False
                sql = """
                        UPDATE `amapcommercialhouseitem` SET `price`=%s WHERE `id`=%s
                """
                cursor.execute(sql, (item['CommercialHousePrice'], item['CommercialHouseId']) )
                self.conn.commit()

            elif isinstance(item, AmapCommercialHouseItem):
                sql = """
                        INSERT INTO `amapcommercialhouseitem` ( `McdonaldsId`, `name`, `address`, `typecode`, `distance`, `adcode`, `location`) 
                        VALUES ( %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (  item['McdonaldsId'], item['CommercialHouseName']
                                      ,item['CommercialHouseAddress'], item['CommercialHouseTypecode'], item['CommercialHouseDistance']
                                      ,item['CommercialHouseAdcode'], item['CommercialHouseLocation']))
                self.conn.commit()

        except Exception:
            print(traceback.format_exc())
            self.conn.rollback()
        finally:
            cursor.close()