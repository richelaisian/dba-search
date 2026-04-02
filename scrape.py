#!/usr/bin/env python3
"""
Scrape DBA.dk for Tal R original artworks (lithographies, paintings, prints).
Filters out posters, merchandise, and non-Tal-R items.
Generates index.html with results.

Uses JSON-LD structured data embedded in DBA search pages.
"""

import urllib.request
import re
import json
import os
import html
from datetime import datetime

SEARCHES = [
    ("Litografi", "tal+r+litografi"),
    ("Maleri", "tal+r+maleri"),
    ("Tryk", "tal+r+tryk"),
    ("Signeret", "tal+r+signeret"),
]

BASE_URL = "https://www.dba.dk/soeg/?soeg={query}"

EXCLUDE_PATTERNS = [
    r"\bplakat\b", r"\bposter\b", r"\bkunstplakat\b", r"\budstillingsplakat\b",
    r"\bkrus\b", r"\bmug\b", r"\bkop\b", r"\bt-shirt\b", r"\bbog\b",
    r"\bbook\b", r"\bmagasin\b", r"\bkatalog\b", r"\bpostkort\b",
    r"\bpude\b", r"\bcushion\b", r"\bopslagstavle\b", r"\bm\.m\.fl\b",
    r"\blundstoem\b", r"\blundst.m\b", r"\bst.ttebillede\b",
]

TAL_R_PATTERN = re.compile(r"tal[\s\-_]*r\b", re.IGNORECASE)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_page(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "da-DK,da;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_json_ld(html_text):
    """Extract listings from JSON-LD CollectionPage data in DBA pages."""
    listings = []
    json_ld_pattern = re.compile(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.DOTALL
    )

    for m in json_ld_pattern.finditer(html_text):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue

        # DBA uses CollectionPage with mainEntity.itemListElement
        if not isinstance(data, dict):
            continue
        if data.get("@type") != "CollectionPage":
            continue

        main_entity = data.get("mainEntity", {})
        items = main_entity.get("itemListElement", [])

        for entry in items:
            item = entry.get("item", entry)
            name = item.get("name", "")
            description = item.get("description", "")
            url = item.get("url", "")
            image = item.get("image", "")

            if isinstance(image, list):
                image = image[0] if image else ""

            offers = item.get("offers", {})
            price_val = offers.get("price", "")
            currency = offers.get("priceCurrency", "DKK")
            price = f"{int(float(price_val)):,} {currency}".replace(",", ".") if price_val else ""

            if url and name:
                listings.append({
                    "title": name,
                    "price": price,
                    "price_num": float(price_val) if price_val else 0,
                    "description": description,
                    "image": image,
                    "url": url,
                    "location": "",
                })

    return listings


def is_excluded(listing):
    text = f"{listing['title']} {listing['description']}".lower()

    if not TAL_R_PATTERN.search(text):
        return True

    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def format_price(price_num):
    """Format price as Danish style: 8.000 DKK"""
    if not price_num:
        return "Pris ikke angivet"
    return f"{int(price_num):,} DKK".replace(",", ".")


def generate_html(all_listings, timestamp):
    cards_html = ""

    if not all_listings:
        cards_html = '<p class="empty">Ingen resultater fundet. Pr&oslash;v igen senere.</p>'
    else:
        for listing in all_listings:
            if listing.get("image"):
                img_html = f'<img src="{html.escape(listing["image"])}" alt="{html.escape(listing["title"])}" loading="lazy" onerror="this.parentElement.innerHTML=\'<div class=no-img>Intet billede</div>\'">'
            else:
                img_html = '<div class="no-img">Intet billede</div>'

            price_display = format_price(listing.get("price_num", 0))
            category_display = listing.get("category", "")

            cards_html += f'''
            <a href="{html.escape(listing["url"])}" target="_blank" rel="noopener" class="card">
                <div class="card-img">{img_html}</div>
                <div class="card-body">
                    <h3>{html.escape(listing["title"])}</h3>
                    <div class="price">{html.escape(price_display)}</div>
                    <span class="badge">{html.escape(category_display)}</span>
                </div>
            </a>'''

    count = len(all_listings)

    return f'''<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tal R &mdash; DBA Originaler</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f0f0f;
    color: #e0e0e0;
    min-height: 100vh;
  }}
  header {{
    background: #1a1a1a;
    border-bottom: 1px solid #333;
    padding: 2rem;
    text-align: center;
  }}
  header h1 {{
    font-size: 1.8rem;
    font-weight: 300;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #fff;
  }}
  header p {{
    color: #888;
    margin-top: 0.5rem;
    font-size: 0.85rem;
  }}
  .meta {{
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 1rem;
    font-size: 0.8rem;
    color: #666;
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
  }}
  .card {{
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    overflow: hidden;
    text-decoration: none;
    color: inherit;
    transition: transform 0.2s, border-color 0.2s;
  }}
  .card:hover {{
    transform: translateY(-4px);
    border-color: #555;
  }}
  .card-img {{
    width: 100%;
    height: 220px;
    overflow: hidden;
    background: #111;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .card-img img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}
  .no-img {{
    color: #444;
    font-size: 0.85rem;
  }}
  .card-body {{
    padding: 1rem;
  }}
  .card-body h3 {{
    font-size: 0.95rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    line-height: 1.4;
    color: #ddd;
  }}
  .price {{
    font-size: 1.1rem;
    font-weight: 600;
    color: #4CAF50;
    margin-bottom: 0.3rem;
  }}
  .badge {{
    display: inline-block;
    margin-top: 0.5rem;
    padding: 2px 8px;
    background: #2a2a2a;
    border-radius: 4px;
    font-size: 0.7rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
  .empty {{
    text-align: center;
    padding: 4rem;
    color: #666;
    grid-column: 1 / -1;
  }}
  @media (max-width: 600px) {{
    .grid {{ padding: 1rem; gap: 1rem; }}
    header {{ padding: 1.5rem 1rem; }}
  }}
</style>
</head>
<body>
<header>
  <h1>Tal R &mdash; Originaler p&aring; DBA</h1>
  <p>Litografier, malerier og tryk &mdash; kun signerede originaler, ingen plakater</p>
  <div class="meta">
    <span>{count} resultater</span>
    <span>Opdateret: {timestamp}</span>
  </div>
</header>
<div class="grid">
{cards_html}
</div>
</body>
</html>'''


def main():
    all_listings = []
    seen_urls = set()

    for category, query in SEARCHES:
        url = BASE_URL.format(query=query)
        print(f"Henter: {category} ({url})")
        try:
            html_text = fetch_page(url)
            listings = parse_json_ld(html_text)
            print(f"  Fundet {len(listings)} annoncer i JSON-LD")

            for listing in listings:
                listing_url = listing["url"].rstrip("/")
                if listing_url in seen_urls:
                    continue
                if is_excluded(listing):
                    continue
                seen_urls.add(listing_url)
                listing["category"] = category
                all_listings.append(listing)
                print(f"  + {listing['title'][:60]} — {format_price(listing['price_num'])}")

        except Exception as e:
            print(f"  Fejl: {e}")

    all_listings.sort(key=lambda l: l.get("price_num", 0), reverse=True)

    timestamp = datetime.now().strftime("%d/%m/%Y kl. %H:%M")
    html_output = generate_html(all_listings, timestamp)

    output_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"\n{'='*50}")
    print(f"Genereret: {output_path}")
    print(f"Antal originaler fundet: {len(all_listings)}")
    print(f"Tidsstempel: {timestamp}")


if __name__ == "__main__":
    main()
