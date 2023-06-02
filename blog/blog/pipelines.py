# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
from hashlib import sha256
from random import randint

import requests

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter  # type: ignore
from scrapy.exceptions import DropItem


class DuplicateFilterPipeline:
    def __init__(self) -> None:
        self.setup()

    def setup(self) -> None:
        self.con = sqlite3.connect("scraped.db")
        self.cur = self.con.cursor()

        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS scraped(
            name TEXT,
            source TEXT
        )
        """
        )

    def insert_record(self, name: str, source: str):
        self.cur.execute(
            """
            INSERT INTO scraped (name, source) VALUES (?, ?)
            """,
            (
                name,
                source,
            ),
        )
        self.con.commit()

    def is_record_exists(self, name: str) -> bool:
        self.cur.execute("SELECT * FROM scraped where name = ?", (name,))
        result = self.cur.fetchone()
        return True if result else False

    def process_item(self, item, spider):
        name: str
        source: str
        name, source = map(ItemAdapter(item).get, ("name", "source"))

        _name = sha256(name.encode()).hexdigest()

        if self.is_record_exists(_name):
            raise DropItem(f"Item name = '{name}' already exists")
        else:
            self.insert_record(_name, source)
            return item


class BlogPipeline:
    headers = {"Content-type": "application/json"}

    def __init__(self, blog_url: str, auth_url: str, credentials: dict) -> None:
        self.blog_url = blog_url
        self.auth_url = auth_url
        self.credentials = credentials
        self.login()

    @classmethod
    def from_crawler(cls, crawler):
        base_url = crawler.settings.get("OCOP_BASE_URL")
        blog_endpoint = crawler.settings.get("OCOP_BLOG_ENDPOINT")
        auth_endpoint = crawler.settings.get("OCOP_AUTH_ENDPOINT")

        db = crawler.settings.get("OCOP_AUTH_DB")
        login = crawler.settings.get("OCOP_AUTH_USER")
        password = crawler.settings.get("OCOP_AUTH_PASSWORD")

        credentials = {
            "login": login,
            "password": password,
            "db": db,
        }

        return cls(
            blog_url=base_url + blog_endpoint,
            auth_url=base_url + auth_endpoint,
            credentials=credentials,
        )

    def login(self) -> None:
        payload = {
            "jsonrpc": "2.0",
            "params": self.credentials,
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
