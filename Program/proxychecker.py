import requests
import time

def check_proxy(proxy):
    url = "http://httpbin.org/ip"
    
    proxy = f"http://{proxy}"

    proxies = {
        "http": proxy,
        "https": proxy
    }

    try:
        start = time.time()
        response = requests.get(url, proxies=proxies, timeout=10)
        end = time.time()

        if response.status_code == 200:
            print(f"[+] Proxy working: {proxy}")
            print(f"IP Retourned: {response.json()['origin']}")
            print(f"Time: {round(end - start, 2)} secondes")
        else:
            print(f"[-] Proxy invalid: {proxy}")

    except requests.exceptions.ProxyError:
        print(f"[-] Proxy error: {proxy}")
    except requests.exceptions.ConnectTimeout:
        print(f"[-] Timeout: {proxy}")
    except Exception as e:
        print(f"[-] Erreur: {e}")

if __name__ == "__main__":
    proxy_input = input("ip:port : ").strip()

    if not proxy_input:
        print("No proxy")
    else:
        check_proxy(proxy_input)
