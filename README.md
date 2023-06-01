# OCOP Scraper Project

## Table of Contents

- [OCOP Scraper Project](#ocop-scraper-project)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [Environment](#environment)

## Install

```ps1
git clone "https://github.com/vyngt/ocop-scraper"
cd "./ocop-scraper"
pipenv install
pipenv shell
```

## Environment

<p>.env file example</p>

```
BASE_URL = "http://localhost:8069"

AUTH_ENDPOINT = "/web/session/authenticate"
AUTH_USER = "<login>"
AUTH_PASSWORD =  "<password>"
AUTH_DB = "<database>"

BLOG_ENDPOINT = "/api/ocop/blog"
```
