from datetime import datetime

import scrapy
from blog.items import BlogItem
from scrapy.http import HtmlResponse


class OCOPSpider(scrapy.Spider):
    name = "ocop"
    allowed_domains = ["langngheviet.com.vn"]
    start_urls = ["https://langngheviet.com.vn/ocop"]

    def parse_detail(self, response: HtmlResponse):
        blog = BlogItem()

        name = r'//*[@id="main"]/div[2]/div/div/div[1]/div[1]/h1/text()'

        description = r'//div[contains(@class, "article-detail-desc")]/text()'
        content = r'//div[@id="__MB_MASTERCMS_EL_3"]/node()'

        _date_xpath = r'//span[@class="article-date"]/span[@class="format_date"]/text()'
        _time_xpath = r'//span[@class="article-date"]/span[@class="format_time"]/text()'

        _datetime = "%s %s" % (
            response.selector.xpath(_time_xpath).get(),
            response.selector.xpath(_date_xpath).get(),
        )

        try:
            blog["datetime"] = datetime.strptime(_datetime, "%H:%M %d/%m/%Y").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            blog["datetime"] = ""

        blog["source"] = response.url
        blog["name"] = response.selector.xpath(name).get()

        _source_link = (
            '<p style="text-align: right;">Nguồn: <a href="%s">%s</a></p>'
            % (response.url, response.url)
        )

        blog["content"] = "<div><b>%s</b></div><div>%s %s</div>" % (
            response.selector.xpath(description).get(),
            "".join(response.selector.xpath(content).getall()),
            _source_link,
        )

        yield blog

    def parse(self, response: HtmlResponse):
        article_xpath = (
            r'//div[@class="hna-section-left lt"]//a[@class="article-image"]/@href'
        )
        for link in response.selector.xpath(article_xpath).getall():
            yield scrapy.Request(link, callback=self.parse_detail)

        next_page_xpath = r'//*[@id="main"]/div[2]/div/div/div[1]/div[2]/div[2]/a[contains(text(), "Sau")]/@href'
        if next_link := response.selector.xpath(next_page_xpath).get():
            yield scrapy.Request(next_link)
