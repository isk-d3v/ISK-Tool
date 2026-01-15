import requests
import json

def ip_lookup(ip):
    url = f"http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        print("Request error:", e)
        return

    if data.get("status") != "success":
        print("Lookup failed:", data.get("message", "Unknown error"))
        return

    print("\n========== IP LOOKUP RESULT ==========")
    print(f"IP Address        : {data.get('query')}")
    print(f"Reverse DNS       : {data.get('reverse')}")
    print(f"Continent         : {data.get('continent')} ({data.get('continentCode')})")
    print(f"Country           : {data.get('country')} ({data.get('countryCode')})")
    print(f"Region            : {data.get('regionName')} ({data.get('region')})")
    print(f"City              : {data.get('city')}")
    print(f"District          : {data.get('district')}")
    print(f"Postal Code       : {data.get('zip')}")
    print(f"Latitude          : {data.get('lat')}")
    print(f"Longitude         : {data.get('lon')}")
    print(f"Timezone          : {data.get('timezone')}")
    print(f"UTC Offset        : {data.get('offset')}")
    print(f"Currency          : {data.get('currency')}")
    print(f"ISP               : {data.get('isp')}")
    print(f"Organization      : {data.get('org')}")
    print(f"ASN               : {data.get('as')}")
    print(f"AS Name           : {data.get('asname')}")
    print(f"Mobile Network    : {data.get('mobile')}")
    print(f"Proxy/VPN         : {data.get('proxy')}")
    print(f"Hosting/DataCenter: {data.get('hosting')}")
    print("=====================================\n")


if __name__ == "__main__":
    ip = input("Enter an IP address: ").strip()
    ip_lookup(ip)
