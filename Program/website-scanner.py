import requests
import time
from urllib.parse import urljoin

TIMEOUT = 8

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )
}

def banner():
    print("=" * 60)
    print("   Simple Web Vulnerability Scanner")
    print("   Auto URL Input Version")
    print("=" * 60)

def log(level, message):
    now = time.strftime("%H:%M:%S")
    print(f"[{now}] [{level}] {message}")

def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/") + "/"

def safe_get(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except requests.RequestException:
        return None

PATHS = [
    "admin/", "login/", "dashboard/",
    "backup/", "uploads/", "api/",
    ".env", "config.php", "phpinfo.php"
]

def scan_paths(base_url):
    log("INFO", "Scanning interesting paths...")
    found = False

    for path in PATHS:
        target = urljoin(base_url, path)
        r = safe_get(target)

        if r and r.status_code == 200:
            found = True
            log("FOUND", f"Path accessible → {target}")

    if not found:
        log("OK", "No interesting paths found")

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "\"><svg/onload=alert(1)>"
]

def scan_xss(base_url):
    log("INFO", "Testing reflected XSS...")
    vulnerable = False

    for payload in XSS_PAYLOADS:
        test_url = base_url + "?q=" + payload
        r = safe_get(test_url)

        if r and payload.lower() in r.text.lower():
            vulnerable = True
            log("VULN", f"Possible XSS → payload: {payload}")

    if not vulnerable:
        log("OK", "No reflected XSS detected")

SQL_PAYLOADS = [
    "'", "\"", "' OR 1=1 --",
    "' OR 'a'='a", "' UNION SELECT NULL--"
]

SQL_ERRORS = [
    "sql syntax", "mysql", "sqlite",
    "postgresql", "ora-", "syntax error"
]

def scan_sqli(base_url):
    log("INFO", "Testing SQL injection...")
    vulnerable = False

    for payload in SQL_PAYLOADS:
        test_url = base_url + "?id=" + payload
        r = safe_get(test_url)

        if not r:
            continue

        body = r.text.lower()
        for error in SQL_ERRORS:
            if error in body:
                vulnerable = True
                log("VULN", f"SQL error with payload: {payload}")
                break

    if not vulnerable:
        log("OK", "No SQL injection detected")

def main():
    banner()
    url = input("\n[?] Enter target URL → ").strip()

    if not url:
        log("ERROR", "No URL provided")
        return

    target = normalize_url(url)
    log("INFO", f"Target set to {target}")

    print()
    scan_paths(target)
    scan_xss(target)
    scan_sqli(target)

    print()
    log("DONE", "Scan finished")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[EXIT] Scan interrupted")