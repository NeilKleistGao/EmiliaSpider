#coding=utf-8
import scrapy
from emilia.items import EmiliaItem
import sys
import re
reload(sys)
sys.setdefaultencoding('gbk')

# url "https://i.pximg.net/img-original/img/2017/10/17/23/09/40/65478228_p0.jpg"

class EmiliaSpider(scrapy.Spider):
    name = "EMT"
    start_urls = ["https://www.pixiv.net/search.php?word=エミリア&order=date_d&p=1"]

    def parse(self, response):
        imgs = response.xpath("//input[@id=\"js-mount-point-search-result-list\"]")
        #print imgs.extract()[0]
        re_url = r"https:\\/\\/i.pximg.net\\/c\\/240x240\\/img-master\\/img\\/(?P<year>[0-9][0-9][0-9][0-9])\\/(?P<mon>[0-9][0-9])\\/(?P<day>[0-9][0-9])\\/(?P<hour>[0-9][0-9])\\/(?P<min>[0-9][0-9])\\/(?P<sec>[0-9][0-9])\\/(?P<pid>[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])_p0_master1200.jpg"
        urls = re.findall(re_url, imgs.extract()[0])
        for i in range(0, len(urls)):
            item = EmiliaItem()
            url = urls[i]
            item["image_urls"] = "https://i.pximg.net/img-original/img/" + url[0] + "/" + url[1] + "/" + url[2] + "/" + url[3] + "/" + url[4] + "/" + url[5] + "/" + url[6] + "_p0.jpg"
            item["name"] = url[6]
            yield item
        temp = response.xpath("//a[@rel=\"next\"]").xpath("@href").extract()
        if len(temp) > 0:
            tpage = "https://www.pixiv.net/search.php" + temp[0]
            yield scrapy.Request(tpage, callback = self.parse)