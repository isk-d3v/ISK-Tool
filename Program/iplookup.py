import requests

def ip_lookup(ip):
    url = f"http://ip-api.com/json/{ip}?fields=66846719"
    response = requests.get(url, timeout=5)
    data = response.json()

    if data.get("status") != "success":
        print("Invalid IP / Api Error")
        return

    print("\nIP Lookup Result")
    print("-" * 30)
    print(f"IP address     : {data.get('query')}")
    print(f"Country        : {data.get('country')} ({data.get('countryCode')})")
    print(f"Region         : {data.get('regionName')}")
    print(f"City           : {data.get('city')}")
    print(f"Postal code    : {data.get('zip')}")
    print(f"Latitude       : {data.get('lat')}")
    print(f"Longitude      : {data.get('lon')}")
    print(f"Timezone       : {data.get('timezone')}")
    print(f"ISP            : {data.get('isp')}")
    print(f"Organization   : {data.get('org')}")
    print(f"ASN            : {data.get('as')}")
    print(f"Mobile network : {data.get('mobile')}")
    print(f"Proxy / VPN    : {data.get('proxy')}")
    print(f"Hosting        : {data.get('hosting')}")

if __name__ == "__main__":
    ip = input("Enter an IP address: ").strip()
    ip_lookup(ip)
