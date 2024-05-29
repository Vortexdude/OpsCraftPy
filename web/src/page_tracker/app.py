# pylint: disable=C0114

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@cache
def redis():
    # pylint: disable=C0116
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))


@app.get("/")
def index():
    # pylint: disable=C0116
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")  # pylint: disable=E1101
        return "Sorry, something went wrong \N{pensive face}", 500
    else:
        return f"This page has been seen {page_views} times."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # nosec
