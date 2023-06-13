from blog.core.spiders import BlogSpider


class OCOPSpider(BlogSpider):
    name = "ocop"
    allowed_domains = ["langngheviet.com.vn"]
    start_urls = ["https://langngheviet.com.vn/ocop"]

    xpath = {
        "item": {
            "name": r'//*[@id="main"]/div[2]/div/div/div[1]/div[1]/h1/text()',
            "content": [
                {
                    "selector": r'//div[contains(@class, "article-detail-desc")]/text()',
                    "full": False,
                },
                {"selector": r'//div[@id="__MB_MASTERCMS_EL_3"]/node()', "full": True},
            ],
            "datetime": {
                "date": r'//span[@class="article-date"]/span[@class="format_date"]/text()',
                "time": r'//span[@class="article-date"]/span[@class="format_time"]/text()',
                "format": "%H:%M %d/%m/%Y",
            },
            "image_urls": [
                r'//div[@class="__MASTERCMS_CONTENT fw f1 mb clearfix"]//img/@src'
            ],
        },
        "page": {
            "detail": r'//div[@class="hna-section-left lt"]//a[@class="article-image"]/@href',
            "next": r'//*[@id="main"]/div[2]/div/div/div[1]/div[2]/div[2]/a[contains(text(), "Sau")]/@href',
        },
    }
