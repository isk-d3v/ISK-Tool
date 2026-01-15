import os
import sys
import re
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)


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

def replace_user(text):
    username = os.environ.get("USERNAME", "Unknown")
    return text.replace("[user]", username)

def colorize(text):
    pattern = re.compile(r"\{(\w+)\}")
    parts = []
    last_pos = 0
    current_color = ""

    matches = list(pattern.finditer(text))
    if not matches:
        return text

    for i, match in enumerate(matches):
        start, end = match.span()
        color_name = match.group(1).lower()

        if start > last_pos:
            content = text[last_pos:start]
            parts.append(f"{current_color}{content}{Style.RESET_ALL}")

        current_color = colors.get(color_name, "")
        last_pos = end

    if last_pos < len(text):
        content = text[last_pos:]
        parts.append(f"{current_color}{content}{Style.RESET_ALL}")

    return "".join(parts)

banner = r"""


{red}                                     ___ ____  _  __          _____           _ 
{bright_red}                                    |_ _/ ___|| |/ /         |_   _|__   ___ | |
{red}                                     | |\___ \| ' /   _____    | |/ _ \ / _ \| |
{bright_red}                                     | | ___) | . \  |_____|   | | (_) | (_) | |
{red}                                    |___|____/|_|\_\           |_|\___/ \___/|_|


"""



page1 = r"""

{red}                            ____________________________________________________________
{red}                            |                                                           |
{red}                            | - DDoS [1]                                                |
{red}                            | - Website Scanner [2]                                     |
{red}                            |                                                           |
{red}                            |                                                           |
{red}                            |                                                           |
{red}                            |                                                           |
{red}                            |                                                           |
{red}                            |                                                           |
{red}                            |                                                           |
{red}                            |___________________________________________________________|
                            
"""



option_files = {
    1: "Program/ddos.py",
    2: "Program/website-scanner.py",
    3: "Program/iplookup.py",
}

def open_python_file(filepath):
    if not os.path.exists(filepath):
        print(colorize(f"Error the file {filepath} does not exist"))
        return
    try:
        subprocess.run([sys.executable, filepath])
    except Exception as e:
        print(colorize(f"Error while executing : {e}"))


def main():
    print(colorize(banner))
    print(colorize(page1))

    while True:
        prompt = replace_user("\n{bright_blue}[user]{green}@{bright_blue}iskpa - ")
        choice = input(colorize(prompt)).strip()
        if choice.lower() == "q":
            print(colorize("Leaving..."))
            sys.exit(0)
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= 25:
                filepath = option_files.get(num)
                print(colorize(f"Opening : {filepath}"))
                open_python_file(filepath)
            else:
                print(colorize("Invalid Option."))
        else:
            print(colorize("Invalid Enter."))

if __name__ == "__main__":
    main()
