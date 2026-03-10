# /// script
# requires-python = ">=3.10"
# dependencies = ["feedparser", "aiohttp"]
# ///
"""Fetch recent articles from Karpathy's curated RSS feeds and output JSON to stdout.

Uses the bundled hn-popular-blogs-2025.opml in the skill directory.
"""

import argparse
import asyncio
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path
from time import mktime

import aiohttp
import feedparser

_OPML = Path(__file__).parent.parent / "hn-popular-blogs-2025.opml"
MAX_ARTICLES = 20


def parse_opml(path: Path) -> list[dict]:
    """Parse OPML file and return list of {text, xmlUrl, htmlUrl}."""
    tree = ET.parse(path)
    feeds = []
    for outline in tree.iter("outline"):
        url = outline.get("xmlUrl")
        if url:
            feeds.append({
                "text": outline.get("text", ""),
                "xmlUrl": url,
                "htmlUrl": outline.get("htmlUrl", ""),
            })
    return feeds


async def fetch_feed(session: aiohttp.ClientSession, feed: dict, sem: asyncio.Semaphore, cutoff: datetime) -> list[dict]:
    """Fetch and parse a single RSS/Atom feed, returning articles newer than cutoff."""
    url = feed["xmlUrl"]
    try:
        async with sem:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                body = await resp.text()
    except Exception as e:
        print(f"[WARN] Failed to fetch {feed['text']} ({url}): {e}", file=sys.stderr)
        return []

    try:
        d = feedparser.parse(body)
    except Exception as e:
        print(f"[WARN] Failed to parse {feed['text']}: {e}", file=sys.stderr)
        return []

    articles = []
    for entry in d.entries:
        published = None
        for attr in ("published_parsed", "updated_parsed"):
            t = getattr(entry, attr, None)
            if t:
                try:
                    published = datetime.fromtimestamp(mktime(t), tz=timezone.utc)
                except (OverflowError, OSError, ValueError):
                    continue
                break

        if published is None or published < cutoff:
            continue

        summary = ""
        if hasattr(entry, "summary"):
            summary = entry.summary[:500]

        articles.append({
            "title": getattr(entry, "title", "(no title)"),
            "link": getattr(entry, "link", ""),
            "author": getattr(entry, "author", ""),
            "source": feed["text"],
            "source_url": feed["htmlUrl"],
            "published": published.isoformat(),
            "summary": summary,
        })

    return articles


async def main(hours: int) -> None:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    feeds = parse_opml(_OPML)
    print(f"[INFO] Parsed {len(feeds)} feeds from OPML, fetching articles newer than {cutoff.isoformat()}", file=sys.stderr)

    sem = asyncio.Semaphore(20)
    all_articles: list[dict] = []

    async with aiohttp.ClientSession(headers={"User-Agent": "karpathy-curated-rss-brief/1.0"}) as session:
        tasks = [fetch_feed(session, f, sem, cutoff) for f in feeds]
        results = await asyncio.gather(*tasks)

    for batch in results:
        all_articles.extend(batch)

    all_articles.sort(key=lambda a: a["published"], reverse=True)
    all_articles = all_articles[:MAX_ARTICLES]
    print(f"[INFO] Found {len(all_articles)} articles in the last {hours}h (capped at {MAX_ARTICLES})", file=sys.stderr)
    json.dump(all_articles, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch recent RSS articles from Karpathy's curated feed list")
    parser.add_argument("--hours", type=int, default=24, help="How many hours back to look (default: 24)")
    args = parser.parse_args()

    if not _OPML.exists():
        print(f"[ERROR] Bundled OPML not found: {_OPML}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(main(args.hours))
