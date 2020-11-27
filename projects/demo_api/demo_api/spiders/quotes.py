import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        json_file = json.loads(response.body)
        quotes = json_file.get("quotes")
        for quote in quotes:
            yield {
                "author": quote.get("author")["name"],
                "tags": quote.get("tags"),
                "text": quote.get("text")
            }
        has_next = json_file.get("has_next")
        if has_next:
            next_page_number = json_file.get("page")
            yield scrapy.Request(url=f"http://quotes.toscrape.com/api/quotes?page={next_page_number + 1}",
                                 callback=self.parse)
