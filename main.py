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
    required_modules = ["colorama"]
    for module in required_modules:
        if not is_module_installed(module):
            install_module(module)

check_requirements()

import os
import re
from colorama import init, Fore, Style

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
                            |                                                           |
                            |___________________________________________________________|
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
}

def open_python_file(filepath):
    if not filepath or not os.path.exists(filepath):
        print(colorize("{red}Error: file not found"))
        return
    try:
        subprocess.run([sys.executable, filepath])
    except Exception as e:
        print(colorize(f"{red}Execution error: {e}"))

def main():
    print(smooth_gradient(banner))
    print(smooth_gradient(page1))
    print(colorize(f"{bright_green}OS detected:{white} {OS_NAME}"))

    while True:
        prompt = replace_user("\n{bright_blue}[user]{green}@{bright_blue}iskpa - ")
        choice = input(colorize(prompt)).strip()

        if choice.lower() == "q":
            print(colorize("{yellow}Leaving..."))
            sys.exit(0)

        if choice.isdigit():
            num = int(choice)
            filepath = option_files.get(num)
            if filepath:
                print(colorize(f"{cyan}Opening:{white} {filepath}"))
                open_python_file(filepath)
            else:
                print(colorize("{red}Invalid option"))
        else:
            print(colorize("{red}Invalid input"))

if __name__ == "__main__":
    main()