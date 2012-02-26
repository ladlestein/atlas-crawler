from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.conf import settings
from rock.items import MineralItem

import csv

class AtlasSpider(CrawlSpider):
    name = 'atlas'
    allowed_domains = ['http://www.mineralienatlas.de/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'.*MineralData\?mineral=.*'), callback='parse_item', follow=False),
    )

    def start_requests(self):
        filename = settings.get("DATAFILE")
        print "filename = ", filename
        print settings
        input = csv.reader(open(filename, 'rb'))
        for line in input:
            yield self.make_request(line)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        i = MineralItem()
        element = hxs.select("//td[p[contains(text(), 'Space Group number')]]/following-sibling::td[1]/p/text()")
        space_group_text = element.extract()[0]
        name = response.meta['name']
        i['name'] = name
        i['spaceGroupNumber'] = space_group_text
        print "mineral %s has space group %s" % (name, space_group_text)
        return i

    url_pattern = 'http://www.mineralienatlas.de/lexikon/index.php/MineralData?mineral=%s&language=english&lang=en'

    def make_request(self, row):
        mineral_name = row[0]
        request = Request(self.url_pattern % mineral_name)
        request.meta['name'] = mineral_name
        return request

