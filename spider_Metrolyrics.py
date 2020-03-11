import re
import scrapy
from scrapy.http import Request
import jsonlines
import json

# List of artists
list_artists = ['ed-sheeran-lyrics.html','camila-cabello-lyrics.html','queen-lyrics.html','eminem-lyrics.html','drake-lyrics.html','post-malone-lyrics.html','khalid-lyrics.html','rihanna-lyrics.html']

# Set up the scrapy spider
class Spider(scrapy.Spider):
    name = 'Scrape_lyrics'
    allowed_domains = ['metrolyrics.com']
    # custom_settings = {'DOWNLOAD_DELAY': 1.0}

    def start_requests(self):
        #iterate through different artists urls
        urls = ['https://www.metrolyrics.com/'+str(artist) for artist in list_artists]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        #step 2: find all their song urls
        songs = response.xpath('//div[@class="content"]//a/@href').getall() ##It includes videos' links
        for song in songs:
            yield Request(song)

        #step 3: scrape the artist, title and lyrics from this page
        lyrics = response.xpath('//p[@class="verse"]//text()').getall()
        lyrics = ' '.join(lyrics)
        title = response.xpath('//h1/text()').getall()
        title = ' '.join(title)
        artist = response.xpath('//div[@id="page"]//div[@class="banner-heading"]/h2//text()').getall()
        artist = ' '.join(artist)

        item = {'artist':artist,
                'title':title,
                'lyrics':lyrics}

        yield item

        with jsonlines.open('lyrics.jsonl', 'a') as fp:
            fp.write(item)
