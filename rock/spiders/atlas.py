from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from rock.items import MineralItem

from csv import csv

class AtlasSpider(CrawlSpider):
    name = 'atlas'
    allowed_domains = ['http://www.mineralienatlas.de/']
    url_pattern = 'http://www.mineralienatlas.de/lexikon/index.php/MineralData?mineral=%s&language=english&lang=en'

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def make_url(row):
        mineral_name = row[0]
        return Request(url_pattern % mineral_name)

    def start_requests(self):
        input = csv.reader(open(filename, 'rb'))
        map(make_url, input)

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
