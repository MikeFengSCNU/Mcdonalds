# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AmapCommercialHouseItem(scrapy.Item):
    # id = scrapy.Field()  # id,用于标记，将数据表该列设为AUTO_INCREMENT，不需要此item了
    McdonaldsId = scrapy.Field()             # 1、该小区对应的麦当劳ID
    CommercialHouseName = scrapy.Field()     # 2、小区名
    CommercialHouseAddress = scrapy.Field()  # 3、小区地址
    CommercialHouseTypecode = scrapy.Field() # 4、小区typecode（即高德地图里面的POI）
    CommercialHouseDistance = scrapy.Field() # 5、小区距离搜索点的距离
    CommercialHouseAdcode = scrapy.Field()   # 6、小区所在地的区码
    CommercialHouseLocation = scrapy.Field() # 7、小区经纬度


class LianjiaCommercialHouseItem(scrapy.Item):
    CommercialHouseId = scrapy.Field()     #id
    CommercialHousePrice = scrapy.Field()  # 小区房价均价


class CommercialHouseItem(scrapy.Item):
    CommercialHouseName = scrapy.Field()        #小区名
    CommercialHouseAddress = scrapy.Field()     #小区地址
    CommercialHouseTypecode = scrapy.Field()    #小区typecode（即高德地图里面的POI）
    CommercialHouseDistance = scrapy.Field()    #小区距离搜索点的距离
    CommercialHouseAdcode = scrapy.Field()      #小区所在地的区码
    CommercialHouseLocation = scrapy.Field()    #小区经纬度

    CommercialHousePrice = scrapy.Field()       #小区价格
    CommercialHouseHouseholds = scrapy.Field()  #小区户数
    CommercialHousePeople = scrapy.Field()      #小区人数
