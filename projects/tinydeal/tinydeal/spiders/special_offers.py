import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com/']
    start_urls = ['https://www.cigabuy.com/consumer-electronics-c-56_75.html']

    def parse(self, response):
        for product in response.xpath("//div[@class='p_box_wrapper']/div"):
            yield {
                'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url': product.xpath(".//a[@class='p_box_title']/@href").get(),
                'discounted_price': product.xpath(".//div[@class='p_box_price cf']/span[1]/text()").get(),
                'original_price': product.xpath(".//div[@class='p_box_price cf']/span[2]/text()").get()
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
