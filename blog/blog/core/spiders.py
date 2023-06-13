"""
Custom Spider
"""
import re
from datetime import datetime
from typing import Any

import scrapy
from blog.items import BlogItem
from scrapy.http import HtmlResponse
from scrapy.spiders import Spider


class BlogSpider(Spider):
    xpath = {
        "item": {
            "name": str,
            "content": list[dict[str, Any]],
            "datetime": {
                "time": str,
                "date": str,
                "format": str,
            },
            "image_urls": list[str],
        },
        "page": {
            "detail": str,
            "next": str,
        },
    }

    base_url: str

    def convert_url(self, link):
        """relative -> absolute"""
        if not link:
            return link

        pattern = r"^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*"

        if not self.base_url or not re.match(pattern, link):
            return link

        _joiner = "" if link[0] == "/" else "/"

        return _joiner.join((self.base_url, link))

    def get_name(self, response: HtmlResponse):
        if self.xpath["item"]["name"]:
            return response.selector.xpath(self.xpath["item"]["name"]).get().strip()
        return ""

    def get_content(self, response: HtmlResponse):
        if not self.xpath["item"]["content"]:
            return ""

        content = ""
        for x in self.xpath["item"]["content"]:
            selector: str = x["selector"]
            full: bool = x["full"]
            if full:
                content += "".join(response.selector.xpath(selector).getall())
            else:
                content += response.selector.xpath(selector).get()

        return content

    def get_datetime(self, response: HtmlResponse):
        _dt = self.xpath["item"]["datetime"]
        if not _dt:
            return ""

        _date = ""
        _time = "00:00:00"

        if _dt["date"]:
            _date = response.selector.xpath(_dt["date"]).get()

        if _dt["time"]:
            _time = response.selector.xpath(_dt["time"]).get()

        _datetime = "%s %s" % (
            _time,
            _date,
        )

        try:
            return datetime.strptime(
                _datetime, self.xpath["item"]["datetime"]["format"]
            ).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return ""

    def get_image_urls(self, response: HtmlResponse):
        result = []
        if exprs := self.xpath["item"]["image_urls"]:
            for expr in exprs:
                for link in response.selector.xpath(expr).getall():
                    result.append(self.convert_url(link))

        return result

    def parse_detail(self, response: HtmlResponse):
        blog = BlogItem()

        blog["datetime"] = self.get_datetime(response)
        blog["source"] = response.url
        blog["name"] = self.get_name(response)

        _source_link = (
            '<p style="text-align: right;">Nguồn bài viết: <a href="%s">%s</a></p>'
            % (response.url, response.url)
        )

        blog["content"] = "<div>%s</div><div>%s</div>" % (
            self.get_content(response),
            _source_link,
        )

        blog["image_urls"] = self.get_image_urls(response)

        yield blog

    def parse(self, response: HtmlResponse):
        article_xpath = self.xpath["page"]["detail"]
        for link in response.selector.xpath(article_xpath).getall():
            yield scrapy.Request(self.convert_url(link), callback=self.parse_detail)

        next_page_xpath = self.xpath["page"]["next"]
        if next_link := response.selector.xpath(next_page_xpath).get():
            yield scrapy.Request(self.convert_url(next_link))
