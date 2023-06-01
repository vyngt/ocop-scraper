# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os
from random import randint

import requests

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter  # type: ignore

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8069")

AUTH_ENDPOINT = os.environ.get("AUTH_ENDPOINT", "/web/session/authenticate")
AUTH_USER = os.environ.get("AUTH_USER", "")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "")
AUTH_DB = os.environ.get("AUTH_DB", "")

BLOG_ENDPOINT = os.environ.get("BLOG_ENDPOINT", "/api/ocop/blog")


class BlogPipeline:
    headers = {"Content-type": "application/json"}

    def __init__(self) -> None:
        self.setup_url()
        self.login()

    def setup_url(self) -> None:
        self.blog_url = BASE_URL + BLOG_ENDPOINT
        self.auth_url = BASE_URL + AUTH_ENDPOINT

    def login(self) -> None:
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "login": AUTH_USER,
                "password": AUTH_PASSWORD,
                "db": AUTH_DB,
            },
            "id": randint(0, 1000000),
        }

        self.cookies = requests.post(
            self.auth_url, json=payload, headers=self.headers
        ).cookies

    def process_item(self, item, spider):
        name, content, source, datetime = map(
            ItemAdapter(item).get, ("name", "content", "source", "datetime")
        )

        data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "data": {
                    "name": name,
                    "content": content,
                    "source": source,
                    "datetime": datetime,
                }
            },
            "id": randint(0, 1000000),
        }

        requests.post(
            self.blog_url, json=data, headers=self.headers, cookies=self.cookies
        )

        return item
