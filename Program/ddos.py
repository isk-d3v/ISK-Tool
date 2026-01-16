import asyncio
import aiohttp
import ssl

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )
}

async def send_request(session, url, index, results, sem):
    async with sem:
        try:
            async with session.get(url):
                results[index - 1] = f"Request {index} -> Sent"
        except Exception as e:
            results[index - 1] = f"Request {index} -> Error ({type(e).__name__})"

async def run_requests(session, url, count, results):
    sem = asyncio.Semaphore(20)  
    tasks = [
        send_request(session, url, i + 1, results, sem)
        for i in range(count)
    ]
    await asyncio.gather(*tasks)

async def loader(stop_event):
    symbols = ["/", "\\"]
    i = 0
    for _ in range(2):  
        if stop_event.is_set():
            break
        print(f"\rLoading {symbols[i % 2]}", end="", flush=True)
        i += 1
        await asyncio.sleep(1)
    print("\rLoading done        ")

async def main():
    url = input("Site Url : ").strip()
    if not url.startswith("http"):
        print("http / https required")
        return

    try:
        count = int(input("How many requests : "))
    except ValueError:
        print("Invalid number")
        return

    results = [None] * count  

    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(limit=50)
    timeout = aiohttp.ClientTimeout(total=10)
    stop_event = asyncio.Event()

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        headers=HEADERS
    ) as session:

        loader_task = asyncio.create_task(loader(stop_event))
        await run_requests(session, url, count, results)
        stop_event.set()
        await loader_task

    for log in results:
        print(log)

if __name__ == "__main__":
    asyncio.run(main())
