# -*- coding: utf-8 -*-
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep
from selenium.common.exceptions import NoSuchElementException


class BooksSeleniumSpider(Spider):
    name = "books_selenium"
    allowed_domains = ["books.toscrape.com"]

    def start_requests(self):
        self.driver=webdriver.Chrome('C:/webdrivers/chromedriver')
        self.driver.get('http://books.toscrape.com')

        sel=Selector(text=self.driver.page_source)
        books=sel.xpath('//h3/a/@href').extract()
        for book in books:
            url='http://books.toscrape.com/catalogue/'+ book
            yield Request(url,callback=self.parse_book)
        while True:
            try:
                next_pg=self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('sleeping for 3s')
                next_pg.click()

                sel=Selector(text=self.driver.page_source)
                books=sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url='http://books.toscrape.com/catalogue/'+ book
                    yield Request(url,callback=self.parse_book)

            except NoSuchElementException:
                self.logger.ingo('no more p ages to load')
                self.driver.quit()
                break


    def parse_book(self,response):
        title=response.css('h1::text').extract_first()
        url=response.request.url
        yield{'title':title,'url':url}


# To get data from the previous code, there are two methods:
#
#
#
# First Method
# Here is the parse function that you can use to get URLs and title for example:
#
#     def parse_book(self, response):
#         title = response.css('h1::text').extract_first()
#         url = response.request.url
#         yield {'title': title, 'url':url}
# As you can see, all what you need is to use is  response.request.url to get the URL of the current request. Actually, you could even use response.url to get the URL from the response, but the former would be more accurate in the case there are redirections. For this website, both would give the same result.
#
# Yes, you should use this code *without* defining anything in items.py. Using a dictionary should be the same as using items.
#
#
#
# Second Method
# If you rather want to use items, your way should work as well. Add the following to items.py under  class BooksCrawlerItem(scrapy.Item)
#
#     url = scrapy.Field()
#     title = scrapy.Field()
# Then in the books.py import from books_crawler.items import BooksCrawlerItem changing the names based on your project.
#
# Then add the following parse function:
#
#     def parse_book(self, response):
#         items = BooksCrawlerItem()
#         title = response.css('h1::text').extract_first()
#         url = response.request.url
#
#         items['title'] = title
#         items['url'] = url
#         yield items
# The items method should work as well. But do not use parts of one way in the other way to avoid unexpected results.
#
