from playwright.sync_api import sync_playwright

url = "https://www.showcasecinemas.co.uk/movies/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(user_agent="Mozilla/5.0 (compatible; RSSFeedBot/1.0)")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(4000)
    html = page.content()
    browser.close()

print(f"HTML length: {len(html)}")
print(f"Contains 'Out Now': {'Out Now' in html}")

idx = html.find('Out Now')
if idx != -1:
    print("--- Context around first 'Out Now' occurrence ---")
    print(html[max(0, idx-1200):idx+300])
else:
    print("'Out Now' not found — trying 'Toy Story'")
    idx2 = html.find('Toy Story')
    if idx2 != -1:
        print(html[max(0, idx2-1200):idx2+300])
    else:
        print("Neither found. First 2000 chars of body:")
        print(html[:2000])
