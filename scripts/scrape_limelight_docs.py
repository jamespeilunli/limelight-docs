#!/usr/bin/env python3
"""Fetch and normalize the official Limelight documentation pages."""

from __future__ import annotations

import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from bs4 import BeautifulSoup


SITEMAP_URL = "https://docs.limelightvision.io/sitemap.xml"
OUTPUT_DIR = Path("build/limelight-source")
PAGE_FILTERS = (
    "/docs/docs-limelight/",
    "/docs/resources/downloads",
)


def fetch(url: str) -> str:
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8", errors="replace")


def list_urls() -> list[str]:
    xml_text = fetch(SITEMAP_URL)
    root = ET.fromstring(xml_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall("sm:url/sm:loc", ns) if loc.text]
    return [url for url in urls if any(marker in url for marker in PAGE_FILTERS)]


def sanitize_slug(url: str) -> str:
    slug = url.replace("https://docs.limelightvision.io/", "")
    slug = slug.strip("/").replace("/", "__")
    return slug or "index"


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_page(url: str) -> dict:
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")

    article = soup.select_one("article")
    if article is None:
        article = soup.body

    title = normalize_text(
        article.find("h1").get_text(" ", strip=True) if article and article.find("h1") else soup.title.get_text(" ", strip=True)
    )

    headings: list[dict] = []
    blocks: list[dict] = []
    if article:
        for node in article.find_all(["h1", "h2", "h3", "p", "li", "pre", "code", "table"]):
            tag = node.name
            text = normalize_text(node.get_text(" ", strip=True))
            if not text:
                continue
            if tag in {"h1", "h2", "h3"}:
                headings.append({"level": tag, "text": text})
            blocks.append({"type": tag, "text": text})

    pagination = {}
    prev_link = soup.select_one("a.pagination-nav__link--prev")
    next_link = soup.select_one("a.pagination-nav__link--next")
    if prev_link and prev_link.get("href"):
        pagination["prev"] = prev_link["href"]
    if next_link and next_link.get("href"):
        pagination["next"] = next_link["href"]

    return {
        "url": url,
        "title": title,
        "headings": headings,
        "blocks": blocks,
        "pagination": pagination,
    }


def main() -> None:
    urls = list_urls()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pages = [extract_page(url) for url in urls]
    pages.sort(key=lambda page: page["url"])

    (OUTPUT_DIR / "pages.json").write_text(json.dumps(pages, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "urls.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"Wrote {len(pages)} pages to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
