from blog.core.spiders import BlogSpider


class KnlamdongSpider(BlogSpider):
    name = "knlamdong"
    allowed_domains = ["khuyennong.lamdong.gov.vn"]
    start_urls = [
        "https://khuyennong.lamdong.gov.vn/quy-trinh-ky-thuat",
    ]

    base_url = "https://khuyennong.lamdong.gov.vn"

    xpath = {
        "item": {
            "name": r"//div[@class='page-header']/h2[@itemprop='name']/text()",
            "content": [
                {"selector": r"//div[@itemprop='articleBody']/node()", "full": True},
            ],
            "datetime": None,
            "image_urls": None,
        },
        "page": {
            "detail": r'//div[@class="blog"]//h2[@itemprop="name"]/a/@href',
            "next": r'//a[contains(text(), "Trang sau")]/@href',
        },
    }
