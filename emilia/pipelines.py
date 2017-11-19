# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib
import urllib2
from emilia import settings

class EmiliaPipeline(object):
    def process_item(self, item, spider):
        path = settings.IMAGES_STORE + "/" + item["name"] + ".jpg"
        request = urllib2.Request(item["image_urls"])
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36")
        request.add_header("Referer", "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + item["name"])
        request.add_header("Accept-Language", "zh-CN,zh;q=0.8")
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            return item
        print "get from " + item["image_urls"]
        fp = open(path, "wb")
        fp.write(response.read())
        fp.close()
        return item