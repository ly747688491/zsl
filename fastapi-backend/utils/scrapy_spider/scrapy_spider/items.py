# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobInfoSpiderItem(scrapy.Item):
    job_name = scrapy.Field()
    job_education = scrapy.Field()
    job_city = scrapy.Field()
    job_experience = scrapy.Field()
    job_salary = scrapy.Field()
    company_name = scrapy.Field()
    company_size = scrapy.Field()
    company_type = scrapy.Field()
    job_tags = scrapy.Field()
    province = scrapy.Field()





