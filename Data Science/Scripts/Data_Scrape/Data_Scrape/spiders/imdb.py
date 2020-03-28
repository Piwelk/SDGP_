# -*- coding: utf-8 -*-
import scrapy
import os
import pandas as pd

class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    dump_path = '../../../Data/Results/movieDetails.csv'
    #allowed_domains = ['imdb.com']
    urlNeg = []
    urlPos = []
    

    with open('../../../../../aclImdb/train/urls_neg.txt') as f1:
        for line in f1:
            urlNeg.append(line[:-13])

    with open('../../../../../aclImdb/train/urls_pos.txt') as f1:
        for line in f1:
            urlPos.append(line[:-13])

    urlAll = urlNeg + urlPos
    urlAll = list(dict.fromkeys(urlAll))

    if os.path.exists(dump_path):
        os.remove(dump_path)
        print('\x1b[0;33;41m' + 'File found & removed ' + dump_path + '!' + '\x1b[0m')

    start_urls = urlAll

    def parse(self, response):
        print('\x1b[1;30;43m' + 'RUNNING-MAIN' + '\x1b[0m')
        print('\x1b[1;35;40m' + response.request.url + '\x1b[0m')

        movieName = response.request.url[-10:-1]
        name = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first()
        year = response.xpath('//span[@id="titleYear"]/a/text()').extract_first()
        rating = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
        genre = response.xpath('//div[@class="subtext"]/a/text()').extract()
        image = response.xpath('//div[@class="poster"]/a/img/@src').extract_first()
        summary = response.xpath('//div[@class="summary_text"]/text()').extract_first()

        print('\x1b[6;30;42m' + movieName + '\x1b[0m')
        print('\x1b[6;30;42m' + name  + '\x1b[0m')
        print('\x1b[6;30;42m' + str(year)  + '\x1b[0m')
        print('\x1b[6;30;42m' + rating  + '\x1b[0m')
        print('\x1b[6;30;42m' + str(genre[:-1])  + '\x1b[0m')
        print('\x1b[6;30;42m' + image  + '\x1b[0m')
        print('\x1b[6;30;42m' + summary  + '\x1b[0m')

        yield {
                'movieName' : movieName,
                'name' : name,
                'year' : year,
                'rating' : rating,
                'genre' : genre,
                'image' : image,
                'summary' : summary
        }