import os, re, sys
from datetime import datetime
from pathlib import Path
from time import mktime

import feedparser
from slugify import slugify  # from python-slugify

# ---- config / feed URL ----
FEED = (
    os.environ.get("FEED_URL")
    or os.environ.get("PODCAST_RSS")
    or (sys.argv[1] if len(sys.argv) > 1 else None)
)
if not FEED:
    raise SystemExit("No FEED_URL/PODCAST_RSS provided")

posts_dir = Path("_posts")
posts_dir.mkdir(exist_ok=True)

# ---- helpers ----
def to_int(v):
    try:
        if v is None or str(v).strip() == "":
            return None
        return int(str(v).strip())
    except Exception:
        return None

def extract_season(entry):
    # <itunes:season> → 'itunes_season'
    for key in ("itunes_season", "season"):
        if key in entry and entry.get(key) not in (None, ""):
            return to_int(entry.get(key))
    return None

def extract_episode(entry):
    # <itunes:episode> → 'itunes_episode'
    for key in ("itunes_episode", "episode"):
        if key in entry and entry.get(key) not in (None, ""):
            return to_int(entry.get(key))
    return None

def sanitize_excerpt(s):
    s = re.sub(r"<.*?>", "", s or "").strip()
    if s:
        s = re.sub(r"\s+", " ", s)[:180]
    return s

# ---- index existing posts by GUID ----
existing = {}  # guid -> {"path": Path, "text": str, "has_season": bool, "has_episode": bool}
for p in posts_dir.glob("*.md"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    mg = re.search(r'^guid:\s*"?(.+?)"?\s*$', text, re.M)
    if mg:
        guid = mg.group(1).strip()
        has_season  = re.search(r'^season:\s*\d+\s*$',  text, re.M) is not None
        has_episode = re.search(r'^episode:\s*\d+\s*$', text, re.M) is not None
        existing[guid] = {"path": p, "text": text, "has_season": has_season, "has_episode": has_episode}

feed = feedparser.parse(FEED)

new_count = 0
updated_count = 0

for e in feed.entries:
    guid = e.get("id") or e.get("guid") or e.get("link")
    title = e.get("title", "Episode")

    # Date
    if e.get("published_parsed"):
        dt = datetime.fromtimestamp(mktime(e.published_parsed))
    elif e.get("updated_parsed"):
        dt = datetime.fromtimestamp(mktime(e.updated_parsed))
    else:
        dt = datetime.utcnow()
    date_str = dt.strftime("%Y-%m-%d")

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
    summary = sanitize_excerpt(e.get("summary", ""))

    # Cover (episode first, then feed fallback)
    cover = ""
    if "image" in e and isinstance(e.image, dict):
        cover = e.image.get("href", "")
    elif e.get("itunes_image"):
        cover = e.itunes_image.get("href", "") if isinstance(e.itunes_image, dict) else e.itunes_image
    if not cover:
        ff = getattr(feed, "feed", {})
        if isinstance(getattr(feed, "image", None), dict):
            cover = feed.image.get("href", "") or feed.image.get("url", "")
        elif isinstance(ff.get("image"), dict):
            cover = ff["image"].get("href", "") or ff["image"].get("url", "")
        elif ff.get("itunes_image"):
            im = ff["itunes_image"]
            cover = im.get("href", "") if isinstance(im, dict) else im

    # Season / Episode
    season  = extract_season(e)   # int or None
    episode = extract_episode(e)  # int or None

    # ---- update existing post (by GUID) ----
    if guid in existing:
        txt = existing[guid]["text"]
        changed = False

        # find front-matter block
        mfm = re.search(r'^---\s*\n(.*?)\n---\s*', txt, re.S | re.M)
        if mfm:
            fm_block = mfm.group(1)

            # add season if missing
            if season is not None and not existing[guid]["has_season"]:
                if re.search(r'^categories:', fm_block, re.M):
                    fm_block = re.sub(r'^(categories:.*)$',
                                      r'\1\nseason: {}'.format(season),
                                      fm_block, flags=re.M)
                else:
                    fm_block += f"\nseason: {season}"
                changed = True

            # add episode if missing
            if episode is not None and not existing[guid]["has_episode"]:
                # insert after season/categories if possible
                if re.search(r'^season:\s*\d+\s*$', fm_block, re.M):
                    fm_block = re.sub(r'^(season:\s*\d+\s*)$',
                                      r'\1\nepisode: {}'.format(episode),
                                      fm_block, flags=re.M)
                elif re.search(r'^categories:', fm_block, re.M):
                    fm_block = re.sub(r'^(categories:.*)$',
                                      r'\1\nepisode: {}'.format(episode),
                                      fm_block, flags=re.M)
                else:
                    fm_block += f"\nepisode: {episode}"
                changed = True

            if changed:
                txt = txt[:mfm.start(1)] + fm_block + txt[mfm.end(1):]
                existing[guid]["path"].write_text(txt, encoding="utf-8")
                updated_count += 1

        continue  # done updating existing—don’t create duplicate

    # ---- create new post file ----
    slug = slugify(title)[:60] or "episode"
    fn = posts_dir / f"{date_str}-{slug}.md"
    if fn.exists():
        continue  # rare collision; skip

    fm = []
    fm.append("---")
    fm.append("layout: episode")
    safe_title = title.replace("'", "''")
    fm.append(f"title: '{safe_title}'")
    fm.append(f"date: {date_str}")
    fm.append("categories: [episodes]")
    if season is not None:
        fm.append(f"season: {season}")
    if episode is not None:
        fm.append(f"episode: {episode}")
    if summary:
        safe_summary = summary.replace("'", "''")
        fm.append(f"excerpt: '{safe_summary}'")
    if dur:
        fm.append(f"duration: '{dur}'")
    if audio:
        fm.append(f"audio_url: '{audio}'")
    if cover:
        fm.append(f"cover: '{cover}'")
    if guid:
        fm.append(f"guid: '{guid}'")
    fm.append("---\n")
    body = "Imported automatically from RSS.\n"

    fn.write_text("\n".join(fm) + body, encoding="utf-8")
    new_count += 1

print(f"Imported {new_count} new episode(s), updated {updated_count} existing with season/episode.")
