# -*- coding: utf-8 -*-
import os
import glob #os and glob module imported for executing close function.
#this function is executed once the spider has completed scraping.used to analyse data,
#send the data file over email or just receive sms message displaying if it has been completely successfully
from scrapy import Spider
from scrapy.http import Request

def product_info(response,value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()

class BooksOnlyScrapySpider(Spider):
    name = 'books_only_scrapy'
    allowed_domains = ['books.toscrape.com']

    #scrapy arguments
    #to run type command:scrapy crawl spidername -a category="url"
    def __init__(self,category):
        self.start_urls=[category]


    def parse(self,response):
        books=response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url=response.urljoin(book)
            yield Request(absolute_url,callback=self.parse_book)
        #process next page
        next_pg_url=response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_pg_url=response.urljoin(next_pg_url)
        yield Request(absolute_next_pg_url)

    def parse_book(self,response):
        title=response.css('h1::text').extract_first()
        price=response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url=response.xpath('//img/@src').extract_first()
        image_url=image_url.replace('../..','http://books.toscrape.com')
        rating=response.xpath('//*[contains(@class,"star-rating")]/@class').extract_first()
        rating=rating.replace('star-rating','')
        description=response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()
        #product info datapoints
        upc=product_info(response,'UPC')
        product_type=product_info(response,'Product type')
        product_without_tax=product_info(response,'Price (excl. tax)')
        product_with_tax=product_info(response,'Price (incl. tax)')
        tax=product_info(response,'Tax')
        avaibility=product_info(response,'Avaibility')
        number_of_reviews=product_info(response,'Number of reviews')

        yield{
            'title':title,
            'price':price,
            'image_url':image_url,
            'rating':rating,
            'description':description,
            'upc':upc,
            'number_of_reviews':number_of_reviews,
            'product_type':product_type,
            'product_without_tax':product_without_tax,
            'product_with_tax':product_with_tax,
            'tax':tax,
            'avaibility':avaibility,
            'number_of_reviews':number_of_reviews
            }
    #close function
    def close(self,reason):
        csv_file=max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file,'mysteryx.csv')
