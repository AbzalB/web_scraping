# final version spider, we call the spider by the name on line 6 not class name
from scrapy import Spider
from scrapy.http import Request
from imdbproject.items import ImdbRatingItem
import re
import csv

class RatingSpider(Spider):
	name = 'ratingspider'
	allowed_urls = ['www.imdb.com'] # changed from allowed_"domains"

	# //*[@id="main"]/div/div[4]/div[3]/div[1]/div[2]
	# print('abc','*'*50)

	start_urls = ["https://www.imdb.com/title/tt0111161/reviews?ref_=tt_ov_rt"]

	def parse(self, response):
		# print('got here')
		page_urls = []
		i = 0
		with open('old_imdb_scraped.csv', newline='') as csvfile:
			moviereader = csv.reader(csvfile, delimiter=',', quotechar='\"')
			for movie in moviereader:
				i += 1
				if i >= 20:
					break
				id = movie[2]
				if id == 'id':
					continue
				page_urls.append(f"https://www.imdb.com/title/{id}/reviews")
		for url in page_urls:
			print(url)
			yield Request(url=url, callback=self.parse_result_page)


	def parse_result_page(self, response):
		for rating in response.css('div.lister-item'):
			item = ImdbRatingItem()
			item['title'] = rating.css('a.title::text').get()
			item['username'] = rating.css('span.display-name-link').css('a::text').get()
			item['text'] = rating.css('div.show-more__control clickable::text').get()
			yield item
		# title = response.xpath('//*[@id="main"]/div/div[4]/div[3]/div[1]/div[2]/h3/a/text()').extract_first()
		# score = response.xpath('//*[@id="main"]/div/div[4]/div[3]/div[1]/div[2]/div[1]/div[1]/span[2]/text()').extract_first()
		# year = response.xpath('//*[@id="main"]/div/div[4]/div[3]/div[1]/div[2]/h3/span[2]/text()').extract_first()
		# mins = response.xpath('//*[@id="main"]/div/div[4]/div[3]/div[2]/div[2]/p[1]/span[3]/text()').extract_first()
		# rating = response.xpath('//*[@id="main"]/div/div[4]/div[3]/div[1]/div[2]/p[1]/span[1]/text()').extract_first()
		# genre = response.xpath('//*[@id="main"]/div/div[4]/div[3]/div[1]/div[2]/p[1]/span[5]/text()').extract_first().strip()
		# gross = response.xpath('//*[@id="main"]/div/div[4]/div[3]/div[1]/div[2]/p[4]/span[5]/text()').extract_first()
		
		# connecting the ImdbprojectItem (and items) from items.py here
		# Initialize a new ImdbprojectItem instance for each movie

		
# explanation from top down:	
# basically, we import spider and the class ImdbprojectItem created from autogenerated items.py
# next, we changed out allowed_domains and start_urls
# in parse, we want to make a function to read in the urls, my case I have 3 because 100 displayed in pages 1,2 and 50 on 3
# for url.... is a for loop to connect with 'parse_result_page' to go through the pages
# notice that a lot is just repetitive  

# Question: how do I get the xpath? simple. 
# 1st right click on the thing you want to inspect
# 2nd: go to the left of it right click 'copy' > copy xpath
# 3rd: make sure you go back to terminal (really it's scrapy shell) to test it out then copy and paste it (use .extract_first())
# 4rd: go back to the variable you care about related to the link aka the thing you're scraping

# 5th paste it
# 6th: at the end of the link, put a slash '/' then put .text() (still inside  in the quotes)
# 7th: put '.extract_first()' outside the quotes; at the end
# bam.

	