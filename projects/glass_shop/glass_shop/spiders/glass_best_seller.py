import scrapy
from scrapy.http import Request


class GlassBestSellerSpider(scrapy.Spider):
    name = 'glass_best_seller'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        for glass in response.xpath("//div[@id='product-lists']/div"):
            url = glass.xpath(".//div[@class='product-img-outer']/a/@href").get()
            image_url = glass.xpath(".//img[@class='lazy d-block w-100 product-img-default']/@data-src").get()
            name = glass.xpath("normalize-space(.//div[@class='p-title']/a/text())").get()
            price = glass.xpath(".//div[@class='p-price']//span/text()").get()
            yield {
                'url': url,
                'image_url': image_url,
                'name': name,
                'price': price
            }

        next_page = response.xpath(
            "//ul[@class='pagination']/li[position() = last()]/a/@href").get()
        if next_page:
            yield Request(url=next_page, callback=self.parse)
