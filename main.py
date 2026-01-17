import sys
import subprocess
import importlib.util
import platform

def is_module_installed(module):
    return importlib.util.find_spec(module) is not None

def install_module(module):
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", module
    ])

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

import os
import re
import webbrowser
from colorama import init, Fore, Style

GITHUB_LINK = "https://github.com/isk-d3v"

DISCORD_LINK = "https://discord.gg/TefpZhrngk"

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

colors = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "bright_black": Fore.LIGHTBLACK_EX,
    "bright_red": Fore.LIGHTRED_EX,
    "bright_green": Fore.LIGHTGREEN_EX,
    "bright_yellow": Fore.LIGHTYELLOW_EX,
    "bright_blue": Fore.LIGHTBLUE_EX,
    "bright_magenta": Fore.LIGHTMAGENTA_EX,
    "bright_cyan": Fore.LIGHTCYAN_EX,
    "bright_white": Fore.LIGHTWHITE_EX,
}

def smooth_gradient(text):
    gradient = [
        172, 178, 184, 190, 226,
        220, 214, 208, 202,
        214, 220, 226, 190, 184, 178
    ]

    result = ""
    idx = 0
    for char in text:
        if char == "\n":
            result += char
            continue
        color_code = gradient[idx % len(gradient)]
        result += f"\033[38;5;{color_code}m{char}"
        idx += 1
    return result + "\033[0m"

def replace_user(text):
    username = os.environ.get("USERNAME") or os.environ.get("USER") or "Unknown"
    return text.replace("[user]", username)

def open_github_link(url):
    try:
        webbrowser.open(url)
        print(colorize("{green}[+] Browser Opened successfully"))
    except Execption as e:
        print(colorize(f"{red}[-] Failed to open browser : {e}"))

def open_discord_link(url):
    try:
        webbrowser.open(url)
        print(colorize("{green}[+] Browser Opened successfully"))
    except Execption as e:
        print(colorize(f"{red}[-] Failed to open browser : {e}"))

def colorize(text):
    pattern = re.compile(r"\{(\w+)\}")
    parts = []
    last_pos = 0
    current_color = ""

    for match in pattern.finditer(text):
        start, end = match.span()
        color_name = match.group(1).lower()

        if start > last_pos:
            parts.append(f"{current_color}{text[last_pos:start]}{Style.RESET_ALL}")

        current_color = colors.get(color_name, "")
        last_pos = end

    if last_pos < len(text):
        parts.append(f"{current_color}{text[last_pos:]}{Style.RESET_ALL}")

    return "".join(parts)

banner = r"""
                                     ___ ____  _  __          _____           _ 
                                    |_ _/ ___|| |/ /         |_   _|__   ___ | |
                                     | |\___ \| ' /   _____    | |/ _ \ / _ \| |
                                     | | ___) | . \  |_____|   | | (_) | (_) | |
                                    |___|____/|_|\_\           |_|\___/ \___/|_|
"""

page1 = r"""
                            Next [N]                                             Back [B]
                            ____________________________________________________________
                            |                                                           |
                            | - DDoS [1]                                                |
                            | - Website Scanner [2]                                     |
                            | - Ip Lookup [3]                                           |
                            | - Python Encryptor [4]                                    |
                            | - Phone Lookup [5]                                        |
                            | - Email Lookup [6]                                        |
                            | - Youtube Lookup [7]                                      |
                            | - Discord Server Lookup [8]                               |
                            | - Website Port Scanner [9]                                |
                            |___________________________________________________________|
                            |  Github Profile [G]      Exit [Q]     Discord Server [D]  |
                          =================================================================
"""

page2 = r"""
                            Next [N]                                             Back [B]
                            ____________________________________________________________
                            |                                                           |
                            | - Website Check [10]                                      |
                            |                                                           |
                            |                                                           |
                            |                                                           |
                            |                                                           |
                            |                                                           |
                            |                                                           | 
                            |                                                           |
                            |                                                           |
                            |___________________________________________________________|
                            |  Github Profile [G]      Exit [Q]     Discord Server [D]  |
                          =================================================================
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
}

ALIASES = {
    "quit": ["q", "Q", "quit", "exit"],
    "github": ["g", "G", "git", "github"],
    "discord": ["d", "D", "dc", "discord"],
    "next": ["n", "N", "next"],
    "back": ["b", "B", "back"]
}

def open_python_file(filepath):
    if not os.path.exists(filepath):
        print(colorize("{red}[-] File not found"))
        return
    subprocess.run([sys.executable, filepath])

def show_page(page):
    os.system("cls" if OS_NAME == "Windows" else "clear")
    print(smooth_gradient(banner))
    print(smooth_gradient(page1 if page == 1 else page2))

def main():
    current_page = 1
    show_page(current_page)

    while True:
        prompt = replace_user("\n{bright_blue}[user]{green}@{bright_blue}iskpa - ")
        choice = input(colorize(prompt)).strip().lower()

        if choice in ALIASES["quit"]:
            print(colorize("{yellow}Leaving..."))
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
            if (current_page == 1 and num > 9) or (current_page == 2 and num > 10):
                print(colorize("{red}[-] Option not available on this page"))
                continue

            filepath = option_files.get(num)
            if filepath:
                print(colorize("{cyan}[+] Opening:{white} {filepath}"))
                open_python_file(filepath)
            else:
                print(colorize("{red}[-] Invalid option"))
        else:
            print(colorize("{red}[-] Invalid input"))

if __name__ == "__main__":
    main()