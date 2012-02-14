# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MineralItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    space_group_number = Field()

