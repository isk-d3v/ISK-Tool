import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCE_URL = "https://free-proxy-list.net/"
TEST_URL = "https://httpbin.org/ip"
TIMEOUT = 5
THREADS = 30
OUTPUT_FILE = "working_proxies.txt"


def scrape_proxies():
    print("[*] Scraping proxies...")
    response = requests.get(SOURCE_URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    proxies = []
    table = soup.find("table", class_="table table-striped table-bordered")
    rows = table.tbody.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        ip = cols[0].text.strip()
        port = cols[1].text.strip()
        is_https = cols[6].text.strip().lower() == "yes"
        scheme = "https" if is_https else "http"
        proxies.append(f"{scheme}://{ip}:{port}")

    print(f"[+] {len(proxies)} proxies found")
    return proxies


def test_proxy(proxy):
    try:
        r = requests.get(
            TEST_URL,
            proxies={
                "http": proxy,
                "https": proxy
            },
            timeout=TIMEOUT
        )
        if r.status_code == 200:
            print(f"[OK] {proxy}")
            return proxy
    except Exception:
        pass
    return None


def main():
    proxies = scrape_proxies()
    working_proxies = []

    print("[*] Testing proxies...")
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(test_proxy, proxy) for proxy in proxies]

        for future in as_completed(futures):
            result = future.result()
            if result:
                working_proxies.append(result)

    with open(OUTPUT_FILE, "w") as f:
        for proxy in working_proxies:
            f.write(proxy + "\n")

    print("\n========== SUMMARY ==========")
    print(f"Working proxies: {len(working_proxies)}")
    print(f"Saved to file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
