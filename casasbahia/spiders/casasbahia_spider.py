# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request


class CasasbahiaSpiderSpider(scrapy.Spider):
    name = 'casasbahia_spider'
    allowed_domains = ['casasbahia.com.br']
    start_urls = ['https://recompra.casasbahia.com.br/smartphone']

    def parse(self, response):
        Make = Selector(response).xpath('//a[@class = "product-image"]/img/@title').extract()
        url = Selector(response).xpath('//a[@class = "product-image"]/@href').extract()
        
        
        for links in url:
            yield Request(links, callback = self.parseA)
            
        
            
    def parseA(self, response):
        model = Selector(response).xpath('//a[@class = "product-image"]/img/@title').extract()
        url = Selector(response).xpath('//a[@class = "product-image"]/@href').extract()
        
        
        for links in url:
            yield Request(links, callback = self.parseB)
  
            
    def parseB(self, response):
        CNN = Selector(response).xpath('//a[@class = "product-image"]/@title').extract()
        url = Selector(response).xpath('//a[@class = "product-image"]/@href').extract()

        
        for links in url:
            yield Request(links, callback = self.parseC)        
          
            
    def parseC(self, response):
        Make_CNN = Selector(response).xpath('//div[@class = "product-title"]/text()').extract()
        
        pattern = r'"id"\:"2"\,"label"\:"Tier Price Matrix 2"\,"price"\:"(\w+)"'
        Prices = Selector(response).xpath('//script[@type = "text/javascript"]').re(pattern) 
        
        url = Selector(response).xpath('//link[@rel = "canonical"]/@href').extract()
        
        
        for item in zip(Make_CNN, url, Prices):
            #create a dictionary to store the scraped info
            scraped_info = {
                'Make_CNN' : item[0],
                'url' : item[1],
                'Prices' : item[2]
            }
    
            #yield or give the scraped info to scrapy
            yield scraped_info

