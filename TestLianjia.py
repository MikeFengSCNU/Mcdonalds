from scrapy import Request
from scrapy.spiders import Spider
from Amap.items import LianjiaCommercialHouseItem


class DoubanMovieTop250Spider(Spider):
    name = 'LianjiaTest'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }

    def start_requests(self):
        # url = 'https://gz.lianjia.com/ershoufang/rs欧洲城/'
        # name = '欧洲城'
        url = 'https://gz.lianjia.com/ershoufang/rs侨鑫·汇景新城龙熹山/'
        name = '侨鑫·汇景新城龙熹山'
        yield Request(url,headers=self.headers)

    def parse(self, response):
        item = LianjiaCommercialHouseItem()
        noresult = response.xpath('//div[@class="m-noresult"]/p/text()') # 没有相关结果
        noresult_lis = response.xpath('//ul[@class="noResultCommunityList"]/li')
        if (noresult != ''):
            print( 'noresult: ', noresult )
            js = response.xpath('/html/body/script[25]/text()')
            print( 'js: ', js )
            # 命令行调试代码，需要调试时把下面两行的代码注释去掉
            from scrapy.shell import inspect_response
            inspect_response(response, self)
            if (noresult_lis != ''):
                for li in noresult_lis:
                    cur_li = li.xpath('.//li[@class="clear"]/div[@class="info"]/div[@class="title"]/a/text()').extract_first()
                    print('cur_li: ', cur_li )
                    # 命令行调试代码，需要调试时把下面两行的代码注释去掉
                    from scrapy.shell import inspect_response
                    inspect_response(response, self)

        # elif ()
        # 命令行调试代码，需要调试时把下面两行的代码注释去掉
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)


