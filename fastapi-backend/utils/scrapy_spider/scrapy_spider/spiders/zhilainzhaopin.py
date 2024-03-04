from typing import Iterable, Any

import scrapy
from scrapy import Request
from scrapy.http import Response
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from utils.scrapy_spider.scrapy_spider.items import JobInfoSpiderItem
from utils.scrapy_spider.setting import HEADERS, COOKIE


def header_row_to_dict(raw_headers):
    headers_dict = {}
    for line in raw_headers.split("\n"):
        if line.strip() == "":
            continue
        key, value = line.split(": ", 1)
        headers_dict[key.strip()] = value.strip()
    return headers_dict


def parsing_urls(url):
    url_parts = urlparse(url)
    # 获取 URL 参数
    params = parse_qs(url_parts.query)
    # 修改参数
    if int(params['p'][0]) + 1 < 30:
        params['p'] = [str(int(params['p'][0]) + 1)]
        # 重新构造 URL
        new_query = urlencode(params, doseq=True)
        new_url_parts = list(url_parts)
        new_url_parts[4] = new_query
        new_url = urlunparse(new_url_parts)
        return new_url
    else:
        return None


class ZhilainzhaopinSpider(scrapy.Spider):
    name = "zhiliannzhaopin"
    allowed_domains = ["sou.zhaopin.com"]
    start_urls = ["https://sou.zhaopin.com/"]
    city_list = {'上海': 538, '北京': 530, '广州': 763, '深圳': 765, '天津': 531, '武汉': 736, '西安': 854,
                 '呼和浩特': 587, '南京': 635, '杭州': 653, '沈阳': 599, '大连': 600}

    def start_requests(self) -> Iterable[Request]:
        self.cookies = {i.split("=")[0]: i.split("=")[1] for i in COOKIE.split("; ")}
        self.headers = header_row_to_dict(HEADERS)

        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            cookies=self.cookies,
            headers=self.headers,
        )

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for city_name in self.city_list.keys():
            city_url = f"https://sou.zhaopin.com/?jl={self.city_list[city_name]}&kw=Python&p=1"
            yield scrapy.Request(
                url=city_url,
                callback=self.parse_page,
                cookies=self.cookies,
                headers=self.headers,
                meta={'province': city_name}
            )

    def parse_page(self, response: Response, **kwargs: Any) -> Any:
        city_name = response.meta.get('province', '未知城市')
        url = response.request.url
        next_page = parsing_urls(url)
        item = JobInfoSpiderItem()
        list_body = response.xpath("//div[@class='joblist-box__item clearfix']")
        for body in list_body:
            item['job_name'] = body.xpath(".//div[@class='jobinfo']/div/span/text()").extract_first().strip()
            item['job_education'] = body.xpath(
                ".//div[@class='jobinfo__other-info']/div[3]/text()").extract_first().strip()
            item['job_city'] = body.xpath(
                ".//div[@class='jobinfo__other-info']/div[1]/span/text()").extract_first().strip()
            item['job_experience'] = body.xpath(
                ".//div[@class='jobinfo__other-info']/div[2]/text()").extract_first().strip()
            item['job_salary'] = body.xpath(".//div[@class='jobinfo']/div/p/text()").extract_first().strip()
            item['job_tags'] = ';'.join(body.xpath(".//div[@class='jobinfo__tag']//div//text()").extract())
            item['company_name'] = body.xpath(
                "//div[@class='companyinfo__top']/div[@class='companyinfo__name']/text()").extract_first().strip()
            item['company_type'] = body.xpath(".//div[@class='companyinfo__tag']/div[1]/text()").extract_first().strip()
            item['company_size'] = body.xpath("//div[@class='companyinfo__tag']/div[2]/text()").extract_first().strip()
            item['province'] = city_name

            yield item

        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_page,
                cookies=self.cookies,
                headers=self.headers,
            )
