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
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=False),
    )

    def start_requests(self):
        filename = settings.get("DATAFILE")
        print "filename = ", filename
        print settings
        input = csv.reader(open(filename, 'rb'))
        return map(make_url, [input.next(), input.next(), input.next()])

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = MineralItem()
        element = hxs.select("//td[p[contains(text(), 'Space Group number')]]/following-sibling::td[1]/p/text()")
        text = element.extract()[0]
        i.name = ""
        i.space_group_number = text
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i

url_pattern = 'http://www.mineralienatlas.de/lexikon/index.php/MineralData?mineral=%s&language=english&lang=en'

def make_url(row):
    mineral_name = row[0]
    return Request(url_pattern % mineral_name)

