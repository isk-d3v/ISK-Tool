from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import socket
import ssl
import requests
from urllib.parse import urlparse
import uvicorn

app = FastAPI()

TARGET_URL = ""
TARGET_HOST = ""

def normalize_url(url):
    url = url.strip()
    if "://" not in url:
        url = "https://" + url
    return url

def dns_lookup(host):
    try:
        return ", ".join(socket.gethostbyname_ex(host)[2])
    except:
        return "Unavailable"

def port_scan(host):
    ports = [21, 22, 25, 53, 80, 110, 143, 443, 3306, 8080]
    open_ports = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                open_ports.append(port)
            s.close()
        except:
            pass
    return open_ports

def ssl_info(host):
    try:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=host)
        s.settimeout(3)
        s.connect((host, 443))
        cert = s.getpeercert()
        s.close()
        return str(cert.get("issuer"))
    except:
        return "Unavailable"

def headers_info(url):
    try:
        r = requests.get(url, timeout=5)
        return "<br>".join(f"{k}: {v}" for k, v in r.headers.items())
    except:
        return "Unavailable"

@app.get("/", response_class=HTMLResponse)
def home():
    ports = port_scan(TARGET_HOST)

    html = f"""
    <html>
    <head>
        <title>Web Check</title>
        <style>
            body {{ font-family: Arial; background: #0f172a; color: #e5e7eb; padding: 30px }}
            h1 {{ font-size: 28px }}
            h2 {{ margin-top: 25px }}
            .box {{ background: #020617; padding: 15px; border-radius: 10px }}
        </style>
    </head>
    <body>
        <h1>Web Check Report</h1>
        <p>Target: {TARGET_HOST}</p>

        <h2>Open Ports</h2>
        <div class="box">
            {" , ".join(str(p) for p in ports) if ports else "No open ports detected"}
        </div>

        <h2>DNS</h2>
        <div class="box">{dns_lookup(TARGET_HOST)}</div>

        <h2>SSL</h2>
        <div class="box">{ssl_info(TARGET_HOST)}</div>

        <h2>Headers</h2>
        <div class="box">{headers_info(TARGET_URL)}</div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    TARGET_URL = input("Target URL: ")
    TARGET_URL = normalize_url(TARGET_URL)

    parsed = urlparse(TARGET_URL)
    TARGET_HOST = parsed.hostname

    if TARGET_HOST is None:
        print("Invalid URL")
        exit()

    uvicorn.run(app, host="127.0.0.1", port=8000)
