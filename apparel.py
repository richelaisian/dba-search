#!/usr/bin/env python3
"""
Generate apparel.html from LeBonCoin scraped data.
Reads data/leboncoin.json (written by the scheduled Claude task via Chrome)
and produces the HTML results page.

JM Weston 180 size 5D equivalents:
  - JM Weston: 5
  - UK: 5.5
  - EU: 38.5 / 39 / 39.5 (depending on last; 180 runs small)
  - US: 6 / 6.5

LeBonCoin shoe_size values for target sizes:
  - "23" = EU 38
  - "57" = EU 37.5  (too small usually)
  - "24" = EU 39
  - "59" = EU 39.5
"""

import json
import os
import html
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(OUTPUT_DIR, "data", "leboncoin.json")

# EU sizes that correspond to JM Weston 5D
TARGET_SIZES = {"38", "38,5", "39", "39,5"}

# Also match by title patterns for JM Weston sizing (e.g. "5D", "5/D", "5 D")
import re
WESTON_SIZE_PATTERN = re.compile(r"\b5[\s/]?[dD]\b")


def format_price_eur(price):
    if not price:
        return "Prix non indiqué"
    return f"{int(price):,} €".replace(",", " ")


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_listings(listings):
    """Filter for target size and JM Weston 180."""
    results = []
    for item in listings:
        eu_size = item.get("shoe_size_eu", "")
        title = item.get("title", "")

        # Check if size matches
        size_match = eu_size in TARGET_SIZES
        # Also check title for Weston-specific sizing
        title_match = bool(WESTON_SIZE_PATTERN.search(title))

        if size_match or title_match:
            results.append(item)

    return results


def generate_html(listings, timestamp):
    cards = ""
    if not listings:
        cards = '<p class="empty">Ingen resultater fundet. Scraping k&oslash;rer dagligt kl. 5:30.</p>'
    else:
        for item in listings:
            img = item.get("image", "")
            if img:
                img_html = f'<img src="{html.escape(img)}" alt="{html.escape(item["title"])}" loading="lazy" onerror="this.parentElement.innerHTML=\'<div class=no-img>No image</div>\'">'
            else:
                img_html = '<div class="no-img">No image</div>'

            price = format_price_eur(item.get("price", 0))
            city = item.get("city", "")
            size = item.get("shoe_size_eu", "")
            condition = item.get("condition", "")

            size_badge = f'<span class="badge size">EU {html.escape(size)}</span>' if size else ''
            cond_badge = f'<span class="badge cond">{html.escape(condition)}</span>' if condition else ''

            cards += f'''
            <a href="{html.escape(item["url"])}" target="_blank" rel="noopener" class="card">
                <div class="card-img">{img_html}</div>
                <div class="card-body">
                    <h3>{html.escape(item["title"])}</h3>
                    <div class="price">{html.escape(price)}</div>
                    <div class="location">{html.escape(city)}</div>
                    <div class="badges">
                        {size_badge}
                        {cond_badge}
                    </div>
                </div>
            </a>'''

    count = len(listings)

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JM Weston 180 &mdash; LeBonCoin</title>
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
  .size-info {{
    background: #1a1a1a;
    border-bottom: 1px solid #222;
    padding: 0.8rem 2rem;
    text-align: center;
    font-size: 0.75rem;
    color: #555;
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
    color: #e67e22;
    margin-bottom: 0.3rem;
  }}
  .location {{
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 0.4rem;
  }}
  .badges {{
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
  .badge.size {{
    background: #1a3a2a;
    color: #4CAF50;
  }}
  .badge.cond {{
    background: #2a2a2a;
    color: #aaa;
  }}
  .empty {{
    text-align: center;
    padding: 4rem;
    color: #666;
    grid-column: 1 / -1;
  }}
  .back-link {{
    display: inline-block;
    margin-top: 0.8rem;
    color: #555;
    font-size: 0.8rem;
    text-decoration: none;
  }}
  .back-link:hover {{
    color: #888;
  }}
  @media (max-width: 600px) {{
    .grid {{ padding: 1rem; gap: 1rem; }}
    header {{ padding: 1.5rem 1rem; }}
  }}
</style>
</head>
<body>
<header>
  <h1>JM Weston 180</h1>
  <p>LeBonCoin &mdash; Taille 5D (EU 38&ndash;39.5)</p>
  <div class="meta">
    <span>{count} resultater</span>
    <span>Opdateret: {timestamp}</span>
  </div>
  <a href="index.html" class="back-link">&larr; DBA Kunst</a>
</header>
<div class="size-info">
  JM Weston 5D = UK 5.5 = EU 38.5&ndash;39.5 = US 6&ndash;6.5
</div>
<div class="grid">
{cards}
</div>
</body>
</html>'''


def main():
    listings = load_data()
    filtered = filter_listings(listings)
    filtered.sort(key=lambda l: l.get("price", 0))

    timestamp = datetime.now().strftime("%d/%m/%Y kl. %H:%M")
    output = generate_html(filtered, timestamp)

    output_path = os.path.join(OUTPUT_DIR, "apparel.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Generated: {output_path}")
    print(f"Total listings in data: {len(listings)}")
    print(f"Matching size 5D (EU 38-39.5): {len(filtered)}")
    print(f"Timestamp: {timestamp}")


if __name__ == "__main__":
    main()
