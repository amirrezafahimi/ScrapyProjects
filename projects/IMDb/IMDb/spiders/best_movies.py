import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/86.0.4240.198 Safari/537.36 "

    def start_requests(self):
        yield scrapy.Request(url="https://www.imdb.com/search/title/?groups=top_250&sort=user_rating",
                             headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True,
             process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"),
             process_request='set_user_agent')
    )

    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='title_wrapper']/h1/text()").get().replace('\xa0', ''),
            'director': response.xpath("(//div[@class='credit_summary_item']/a/text())[1]").get(),
            'year': response.xpath("//span[@id='titleYear']/a/text()").get(),
            'run_time': response.xpath("normalize-space((//time)[1]/text())").get(),
            'genre': response.xpath("(//div[@class='subtext']/a[1]/text())[1]").get(),
            'rating': response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            # 'country': response.xpath("(//div[@class='txt-block'])[9]/a/text()").get(),
            # 'budget': response.xpath("(//div[@class='txt-block'])[14]/h4/following-sibling::text()[1]").get().strip(),
            # 'gross': response.xpath("(//div[@class='txt-block'])[17]/h4/following-sibling::text()[1]").get().strip(),
            'movie_url': response.url,
            'movie_imdb_id': response.url.split('/')[-2]
        }
