import os, re, sys
from datetime import datetime
from pathlib import Path

import feedparser
from slugify import slugify  # pip install python-slugify

FEED = (
    os.environ.get("FEED_URL")
    or os.environ.get("PODCAST_RSS")
    or (sys.argv[1] if len(sys.argv) > 1 else None)
)
if not FEED:
    raise SystemExit("No FEED_URL/PODCAST_RSS provided")

posts_dir = Path("_posts")
posts_dir.mkdir(exist_ok=True)

# Track existing GUIDs so we don't duplicate within a build
existing_guids = set()
for p in posts_dir.glob("*.md"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'^guid:\s*"?(.+?)"?\s*$', text, re.M)
    if m:
        existing_guids.add(m.group(1).strip())

feed = feedparser.parse(FEED)
new_count = 0

for e in feed.entries:
    guid = e.get("id") or e.get("guid") or e.get("link")
    if guid and guid in existing_guids:
        continue

    title = e.get("title", "Episode")
    # Date
    dt = None
    if e.get("published_parsed"): dt = datetime(*e.published_parsed[:6])
    elif e.get("updated_parsed"): dt = datetime(*e.updated_parsed[:6])
    else: dt = datetime.utcnow()
    date_str = dt.strftime("%Y-%m-%d")

    # Slug & filename
    slug = slugify(title)[:60] or "episode"
    fn = posts_dir / f"{date_str}-{slug}.md"
    if fn.exists():
        continue

    # Audio enclosure
    audio = ""
    if e.get("links"):
        for l in e.links:
            if l.get("rel") == "enclosure":
                audio = l.get("href", "")
                break
    if not audio and e.get("enclosures"):
        audio = e.enclosures[0].get("href", "")

    # Duration / summary
    dur = e.get("itunes_duration") or ""
    summary = re.sub(r"<.*?>", "", e.get("summary", "")).strip()
    if summary:
        summary = re.sub(r"\s+", " ", summary)[:180]

    # Cover (many feeds use itunes:image)
    cover = ""
    if "image" in e and isinstance(e.image, dict):
        cover = e.image.get("href", "")
    elif e.get("itunes_image"):
        cover = e.itunes_image.get("href", "") if isinstance(e.itunes_image, dict) else e.itunes_image

    # Write front matter
    fm = []
    fm.append("---")
    fm.append("layout: episode")
    fm.append(f'title: "{title.replace(\'"\', r\'\\\"\')}"')
    fm.append(f"date: {date_str}")
    fm.append("categories: [episodes]")
    if summary: fm.append(f'excerpt: "{summary}"')
    if dur: fm.append(f'duration: "{dur}"')
    if audio: fm.append(f'audio_url: "{audio}"')
    if cover: fm.append(f'cover: "{cover}"')
    if guid: fm.append(f'guid: "{guid}"')
    fm.append("---\n")
    body = "Imported automatically from RSS.\n"

    fn.write_text("\n".join(fm) + body, encoding="utf-8")
    new_count += 1

print(f"Imported {new_count} new episode(s).")
