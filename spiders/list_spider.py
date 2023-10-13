import scrapy
import re

class ListSpider(scrapy.Spider):
    name= 'list'
    # pagelimit=0

    def __init__(self, link=None, pagelimit=0):
        self.pagelimit=int(pagelimit)
        if link!=None:
            self.start_urls=[link]
        else:
            pass

    # def parse(self, response):
    #     for item in response.css("div.s-item__wrapper"):
    #         if (item.css("img.s-item__image-img::attr(data-src)").get() != None):
    #             img_src= item.css("img.s-item__image-img::attr(data-src)").get()
    #         else:
    #             img_src= item.css("img.s-item__image-img::attr(src)").get()
    #         if (item.css("h3.s-item__title::text").get()==None):
    #             item_name= item.css("h3.s-item__title span.BOLD::text").get()
    #         else:
    #             item_name= item.css("h3.s-item__title::text").get()
    #         yield{
    #             "img_src": img_src,
    #             "item_name": item_name,
    #             "item_price": item.css("span.s-item__price::text").getall(),
    #             "item_link": item.css("a.s-item__link::attr(href)").get()
    #         }
    #     next_page= response.css("nav.pagination a::attr(href)").getall()[1]
    #     if next_page is not None:
    #         yield response.follow(next_page, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links= response.css("a.s-item__link::attr(href)").getall()
        yield from response.follow_all(links, self.parse_item)

        next_page= response.css("nav.pagination a::attr(href)").getall()[1]

        pageno=int(response.css(".pagination__items a[href='#']::text").get())

        if next_page is not None:
            if self.pagelimit!=0 and pageno<=self.pagelimit:
                yield response.follow(next_page, callback=self.parse)
    
    def parse_item(self, response):
        yield{
        "title":response.css(".x-item-title__mainTitle span::text").get(),
        "condition": response.css(".x-item-condition-text span::text").get(),
        "ends-in": response.css(".ux-timer__text ::text").get(),
        "available": str(response.css(".d-quantity__availability span::text").getall()),
        "price": response.css(".x-price-primary span::text").get(),
        }