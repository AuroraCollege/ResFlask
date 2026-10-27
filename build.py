import shutil
from pathlib import Path

from flask import url_for

import parser

# Regenerate the CSVs from com.csv before app is imported, since app loads them on import
parser.parse()

from app import app, r  # noqa: E402

OUT = Path("public")


def pages():
    yield url_for("index")
    yield url_for("full")
    for number in r.staff:
        yield url_for("staff", number=number)
    for year in r.groups:
        yield url_for("group", year=year)
    for site in ["Narrabeen", "Collaroy"]:
        yield url_for("maps", site=site)


def build():
    shutil.rmtree(OUT, ignore_errors=True)
    client = app.test_client()
    with app.test_request_context():
        urls = list(pages())
    for url in urls:
        response = client.get(url)
        if response.status_code != 200:
            raise SystemExit(f"{url} returned {response.status_code}")
        # Each page becomes <url>/index.html so /staff/3/ works on a static host
        path = OUT / url.strip("/") / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.data)
    print(f"Built {len(urls)} pages into {OUT}/")


if __name__ == "__main__":
    build()
