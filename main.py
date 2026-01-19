import sys
import subprocess
import importlib.util
import platform
import os
import re
import webbrowser
import time
from colorama import init, Fore, Style


def is_module_installed(module):
    return importlib.util.find_spec(module) is not None

def install_module(module):
    subprocess.check_call([sys.executable, "-m", "pip", "install", module])

def check_requirements():
    required_modules = {
        "colorama": "colorama",
        "requests": "requests",
        "aiohttp": "aiohttp",
        "customtkinter": "customtkinter",
        "phonenumbers": "phonenumbers",
        "email_validator": "email-validator",
        "dns": "dnspython",
        "bs4": "beautifulsoup4",
        "yt_dlp": "yt-dlp",
        "flask": "flask",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "wheel": "wheel"
    }

    for import_name, pip_name in required_modules.items():
        if not is_module_installed(import_name):
            print(f"[+] Installing {pip_name}...")
            install_module(pip_name)

check_requirements()


init(autoreset=True)

def detect_os():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    elif system == "Darwin":
        return "macOS"
    return "Unknown"

OS_NAME = detect_os()


def blue_gradient(index):
    gradient = [
        18, 19, 20, 21,    
        27, 26, 25, 24,     
        33, 32, 31,        
        26, 25, 24, 21, 20 
    ]
    return gradient[index % len(gradient)]



def animated_draw_gradient(text, delay=0.002):
    idx = 0

    for char in text:
        if char == "\n":
            print()
            continue

        color = blue_gradient(idx)
        sys.stdout.write(f"\033[38;5;{color}m{char}")
        sys.stdout.flush()

        idx += 1
        time.sleep(delay)

    print(Style.RESET_ALL)




def replace_user(text):
    username = os.environ.get("USERNAME") or os.environ.get("USER") or "Unknown"
    return text.replace("[user]", username)


GITHUB_LINK = "https://github.com/isk-d3v"
DISCORD_LINK = "https://discord.gg/TefpZhrngk"

def open_link(url):
    try:
        webbrowser.open(url)
        print(Fore.GREEN + "[+] Browser opened successfully")
    except Exception as e:
        print(Fore.RED + f"[-] Failed to open browser: {e}")


banner = r"""
                                     ___ ____  _  __          _____           _ 
                                    |_ _/ ___|| |/ /         |_   _|__   ___ | |
                                     | |\___ \| ' /   _____    | |/ _ \ / _ \| |
                                     | | ___) | . \  |_____|   | | (_) | (_) | |
                                    |___|____/|_|\_\           |_|\___/ \___/|_|
"""

page1 = r"""
                           Next [N]                                             Back [B]
                          ╭───────────────────────────────────────────────────────────╮
                          │                                                           │
                          │ - DDoS [1]                                                │
                          │ - Website Scanner [2]                                     │
                          │ - Ip Lookup [3]                                           │
                          │ - Python Encryptor [4]                                    │
                          │ - Phone Lookup [5]                                        │
                          │ - Email Lookup [6]                                        │
                          │ - Youtube Lookup [7]                                      │
                          │ - Discord Server Lookup [8]                               │
                          │ - Website Port Scanner [9]                                │
                          │───────────────────────────────────────────────────────────│
                          │  Github Profile [G]      Exit [Q]     Discord Server [D]  │
                          ╰───────────────────────────────────────────────────────────╯
"""

page2 = r"""
                           Next [N]                                             Back [B]
                          ╭───────────────────────────────────────────────────────────╮
                          │                                                           │
                          │ - Website Checker [10]                                    │
                          │ - Website Cloner [11]                                     │
                          │ - Proxy Scraper [12]                                      │
                          │                                                           │
                          │                                                           │
                          │                                                           │
                          │                                                           │
                          │                                                           │
                          │                                                           │
                          │───────────────────────────────────────────────────────────│
                          │  Github Profile [G]      Exit [Q]     Discord Server [D]  │
                          ╰───────────────────────────────────────────────────────────╯
"""

option_files = {
    1: "Program/ddos.py",
    2: "Program/website-scanner.py",
    3: "Program/iplookup.py",
    4: "Program/pyencryptor.py",
    5: "Program/phonelookup.py",
    6: "Program/emaillookup.py",
    7: "Program/youtubelookup.py",
    8: "Program/discordlookup.py",
    9: "Program/websiteportscanner.py",
    10: "Program/websitecheck.py",
    11: "Program/websitecloner.py",
    12: "Program/proxyscraper.py"
}

ALIASES = {
    "quit": ["q", "quit", "exit"],
    "github": ["g", "git", "github"],
    "discord": ["d", "dc", "discord"],
    "next": ["n", "next"],
    "back": ["b", "back"]
}


def open_python_file(filepath):
    if not os.path.exists(filepath):
        print(Fore.RED + "[-] File not found")
        return
    subprocess.run([sys.executable, filepath])

def show_page(page):
    os.system("cls" if OS_NAME == "Windows" else "clear")

    print(Fore.BLUE + banner + Style.RESET_ALL)

    if page == 1:
        animated_draw_gradient(page1)
    else:
        animated_draw_gradient(page2)


def main():
    current_page = 1
    show_page(current_page)

    while True:
        prompt = replace_user(f"\n{Fore.BLUE}[user]{Fore.WHITE}@{Fore.BLUE}iskpa ➜ ")
        choice = input(prompt).strip().lower()

        if choice in ALIASES["quit"]:
            print(Fore.YELLOW + "Leaving...")
            sys.exit(0)

        if choice in ALIASES["github"]:
            open_link(GITHUB_LINK)
            continue

        if choice in ALIASES["discord"]:
            open_link(DISCORD_LINK)
            continue

        if choice in ALIASES["next"] and current_page == 1:
            current_page = 2
            show_page(current_page)
            continue

        if choice in ALIASES["back"] and current_page == 2:
            current_page = 1
            show_page(current_page)
            continue

        if choice.isdigit():
            num = int(choice)
            filepath = option_files.get(num)
            if filepath:
                print(Fore.CYAN + f"[+] Opening: {filepath}")
                open_python_file(filepath)
            else:
                print(Fore.RED + "[-] Invalid option")
        else:
            print(Fore.RED + "[-] Invalid input")

if __name__ == "__main__":
    main()
