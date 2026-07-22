import re
import os
from playwright.sync_api import sync_playwright

url = "https://www.showcasecinemas.co.uk/movies/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(user_agent="Mozilla/5.0 (compatible; RSSFeedBot/1.0)")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(4000)
    html = page.content()
    browser.close()

pattern = re.compile(
    r'href="(/movies/[^"]+)"[^>]*>.*?srcset="(https://[^\s"]+)\s.*?'
    r'<span class="css-efkg2u">([^<]+)</span></h2>'
    r'<span class="css-1mzdl2j">([^<]+)</span>',
    re.DOTALL
)

all_matches = pattern.findall(html)

# only keep movies tagged exactly "Out Now"
matches = [m for m in all_matches if m[3].strip() == "Out Now"][:5]

print(f"Total cards found: {len(all_matches)}")
print(f"Found {len(matches)} 'Out Now' movies")

q = chr(34)
items_xml = ""

for href, poster, title, status in matches:
    title_clean = title.strip().replace("&", "&amp;")
    link = f"https://www.showcasecinemas.co.uk{href}"
    items_xml += "<item>"
    items_xml += f"<title>{title_clean}</title>"
    items_xml += "<description>" + chr(60) + "![CDATA[" + \
        f'<img src=' + q + poster + q + '>' + \
        "]]" + chr(62) + "</description>"
    items_xml += f"<link>{link}</link>"
    items_xml += "</item>"

rss = '<?xml version=' + q + '1.0' + q + ' encoding=' + q + 'UTF-8' + q + '?>'
rss += "<rss version=" + q + "2.0" + q + ">"
rss += "<channel>"
rss += "<title>Now in Cinema</title>"
rss += "<link>https://foxyoo5.github.io/Showcase-Now-Playing/now-playing.xml</link>"
rss += "<description>Movies currently in cinemas from Showcase Cinemas</description>"
rss += items_xml
rss += "</channel></rss>"

os.makedirs("docs", exist_ok=True)
with open("docs/now-playing.xml", "w", encoding="utf-8") as f:
    f.write(rss)
