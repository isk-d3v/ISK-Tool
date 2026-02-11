import requests
import os
from colorama import Fore, Style, init
import fade
from datetime import datetime
from collections import defaultdict
import json
import requests
import hashlib

init(autoreset=True)

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def ascii_logo():
    logo = f"""\n
██╗   ██╗███████╗███████╗██████╗ 
██║   ██║██╔════╝██╔════╝██╔══██╗
██║   ██║███████╗█████╗  ██████╔╝
██║   ██║╚════██║██╔══╝  ██╔══██╗
╚██████╔╝███████║███████╗██║  ██║
 ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
                                 
            {Style.BRIGHT}by o3gy
    """
    print(fade.purpleblue(logo))


def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %B %Y, %H:%M")
    except:
        return "N/A"

def check_rate_limit(response):
    if response.status_code == 403:
        try:
            data = response.json()
            if "API rate limit exceeded" in data.get("message", ""):
                print(Fore.RED + Style.BRIGHT + "❌ GitHub API rate limit exceeded. Please wait before retrying.")
                return True
        except:
            pass
    return False

CACHE_DIR = "./.cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# --- UTILS ---
def format_date(date_str):
    if not date_str:
        return "N/A"
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")
    except:
        return date_str

def get_cache_path(key):
    hashed = hashlib.md5(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hashed}.json")

def cached_fetch(url, headers=None):
    path = get_cache_path(url)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return data
    except:
        pass
    return None


def check_rate_limit(res):
    if res.status_code == 403:
        print("Rate limit exceeded. Try again later.")
        exit()

def get_user_info(username):
    url = f"https://api.github.com/users/{username}"
    data = cached_fetch(url)
    return data if data else None

def get_email_from_commits(username):
    try:
        repos = get_paginated_data(f"https://api.github.com/users/{username}/repos")
        for repo in repos:
            commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits"
            commits = cached_fetch(commits_url)
            if isinstance(commits, list) and commits:
                author = commits[0].get("commit", {}).get("author", {})
                email = author.get("email", "")
                name = author.get("name", "")
                if email:
                    return name, email
    except:
        pass
    return "N/A", "N/A"

def get_paginated_data(url, headers=None):
    results = []
    page = 1
    while True:
        paged_url = f"{url}?per_page=100&page={page}"
        data = cached_fetch(paged_url, headers)
        if not data:
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results

def get_user_orgs(username):
    return get_paginated_data(f"https://api.github.com/users/{username}/orgs")

def count_total_stars(repos):
    return sum(repo.get("stargazers_count", 0) for repo in repos)

def count_starred_projects(username):
    starred = get_paginated_data(f"https://api.github.com/users/{username}/starred")
    return len(starred)

def get_subscriptions(username):
    return get_paginated_data(f"https://api.github.com/users/{username}/subscriptions")

def save_list_to_file(username, data_type, data):
    if not data:
        return False
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{data_type}.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for i, item in enumerate(data, 1):
                f.write(f"{i:02d} - {item['login']} ({item['html_url']})\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de {data_type}: {e}")
        return False

def save_repos_to_file(username, repos):
    if not repos:
        return False
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "repos.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for i, repo in enumerate(repos, 1):
                f.write(f"{i:02d} - {repo['name']} ({repo['html_url']})\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des repos: {e}")
        return False

def save_gists_to_file(username, gists):
    if not gists:
        return False
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "gists.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for i, gist in enumerate(gists, 1):
                f.write(f"{i:02d} - {gist['description'] or 'No Description'} ({gist['html_url']})\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des gists: {e}")
        return False

def save_user_stars(username, repos):
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "star-user.txt")
    headers = {"Accept": "application/vnd.github.v3.star+json"}
    try:
        with open(path, "w", encoding="utf-8") as f:
            for repo in repos:
                api_url = f"https://api.github.com/repos/{username}/{repo['name']}/stargazers"
                page = 1
                entry_count = 0
                while True:
                    paged_url = f"{api_url}?per_page=100&page={page}"
                    data = cached_fetch(paged_url, headers)
                    if not data:
                        break
                    if entry_count == 0:
                        f.write(f"\n--- {repo['name']} ({repo['html_url']}) ---\n")
                    for entry in data:
                        user = entry.get("user", {})
                        starred_at = format_date(entry.get("starred_at"))
                        entry_count += 1
                        f.write(f"{entry_count:02d} - {user.get('login')} ({user.get('html_url')}) → Date: {starred_at}\n")
                    if len(data) < 100:
                        break
                    page += 1
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de user-star: {e}")
        return False

def save_starred_projects(username):
    url = f"https://api.github.com/users/{username}/starred"
    headers = {
        "Accept": "application/vnd.github.v3.star+json"
    }
    starred = get_paginated_data(url, headers=headers)
    
    if not starred:
        print("Aucun projet étoilé trouvé.")
        return False

    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "star-projet.txt")

    try:
        grouped = defaultdict(list)
        for item in starred:
            repo = item.get("repo") or item
            starred_at = item.get("starred_at", "N/A")
            grouped[repo["owner"]["login"]].append((repo, starred_at))

        with open(path, "w", encoding="utf-8") as f:
            for owner, repos in grouped.items():
                f.write(f"\n--- {owner} ---\n")
                for i, (repo, starred_at) in enumerate(repos, 1):
                    desc = repo.get("description", "No description")
                    date_str = format_date(starred_at)
                    f.write(f"{i:02d} - {repo['full_name']} ({repo['html_url']}) → {desc} | Date: {date_str}\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de projet-star: {e}")
        return False

def save_orgs_to_file(username, orgs):
    if not orgs:
        return False
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "orgs.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for i, org in enumerate(orgs, 1):
                name = org.get("login", "N/A")
                url = org.get("html_url", "N/A")
                desc = org.get("description", "No description")
                f.write(f"{i:02d} - {name} ({url}) → {desc}\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des organisations: {e}")
        return False

def save_subscriptions_to_file(username, subscriptions):
    if not subscriptions:
        return False
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "subscriptions.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            for i, repo in enumerate(subscriptions, 1):
                f.write(f"{i:02d} - {repo['full_name']} ({repo['html_url']})\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des subscriptions: {e}")
        return False

def get_languages_stats(username):
    repos = get_paginated_data(f"https://api.github.com/users/{username}/repos")
    lang_bytes = defaultdict(int)
    for repo in repos:
        languages_url = repo.get("languages_url")
        if languages_url:
            langs = cached_fetch(languages_url)
            if langs:
                for lang, bytes_count in langs.items():
                    lang_bytes[lang] += bytes_count
    sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)
    top_langs = [lang for lang, _ in sorted_langs[:3]]
    return top_langs if top_langs else ["n/a"]

def save_user_events(username):
    events = get_paginated_data(f"https://api.github.com/users/{username}/events")
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "events.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"--- GitHub Events for {username} ---\n")
            for i, event in enumerate(events, 1):
                event_type = event.get("type", "Unknown")
                repo = event.get("repo", {}).get("name", "Unknown repo")
                created_at = format_date(event.get("created_at"))
                f.write(f"{i:03d} - [{event_type}] on {repo} at {created_at}\n")
        return len(events)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des events: {e}")
        return 0

def save_received_events(username):
    events = get_paginated_data(f"https://api.github.com/users/{username}/received_events")
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "received_events.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"--- Received GitHub Events for {username} ---\n")
            for i, event in enumerate(events, 1):
                actor = event.get("actor", {}).get("login", "Unknown")
                event_type = event.get("type", "Unknown")
                repo = event.get("repo", {}).get("name", "Unknown repo")
                created_at = format_date(event.get("created_at"))
                f.write(f"{i:03d} - [{event_type}] by {actor} on {repo} at {created_at}\n")
        return len(events)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des received events: {e}")
        return 0

def save_user_info(username, user, name, email, total_stars, projet_stars, top_languages, events, received_events):
    folder = f"./{username}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "info.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"👤 Username: {user.get('login')}\n")
            f.write(f"📝 Name: {user.get('name')}\n")
            f.write(f"🆔 ID: {user.get('id')}\n")
            f.write(f"🧬 Node ID: {user.get('node_id')}\n")
            f.write(f"📧 Email: {email}\n")
            f.write(f"📍 Location: {user.get('location')}\n")
            f.write(f"🧾 Bio: {user.get('bio')}\n")
            f.write(f"💼 Company: {user.get('company')}\n")
            f.write(f"🔗 Blog: {user.get('blog')}\n")
            twitter = user.get("twitter_username")
            if twitter:
                f.write(f"🐦 Twitter: @{twitter} → https://twitter.com/{twitter}\n")
            else:
                f.write("🐦 Twitter: N/A\n")
            f.write(f"📦 Public Repos: {user.get('public_repos')}\n")
            f.write(f"📄 Public Gists: {user.get('public_gists')}\n")
            f.write(f"👥 Followers: {user.get('followers')}\n")
            f.write(f"🏷 Following: {user.get('following')}\n")
            f.write(f"⭐ User Stars: {total_stars}\n")
            f.write(f"⭐ Projet Stars: {projet_stars}\n")
            f.write(f"📅 Events: {events}\n")
            f.write(f"📃 Received Events: {received_events}\n")
            f.write(f"🌐 Top Languages: {','.join(top_languages) if top_languages else 'N/A'}\n")
            f.write(f"✅ Hireable: {user.get('hireable')}\n")
            f.write(f"🗓️ Created At: {format_date(user.get('created_at'))}\n")
            f.write(f"⏱️ Updated At: {format_date(user.get('updated_at'))}\n")
            f.write(f"🖼️ Avatar URL: {user.get('avatar_url')}\n")
            f.write(f"🔗 GitHub URL: {user.get('html_url')}\n")
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'info utilisateur: {e}")
        return False


def main():
    while True:
        clear_console()
        ascii_logo()

        username = input(fade.fire("🔎 Enter GitHub username: ")).strip()
        if not username:
            print(Fore.RED + "❌️ No username entered.")
            input(Fore.YELLOW + "➡️ Press Enter to retry.")
            continue

        print("\n")
        print(Fore.LIGHTCYAN_EX + "⏳ Fetching user data...")
        user = get_user_info(username)
        if not user:
            print(Fore.RED + "❌ User not found.")
            input(Fore.YELLOW + "Press Enter to retry.")
            continue

        name, email = get_email_from_commits(username)
        repos = get_paginated_data(f"https://api.github.com/users/{username}/repos")
        user_stars = count_total_stars(repos)
        projet_stars = count_starred_projects(username)
        top_languages = get_languages_stats(username)
        subscriptions = get_subscriptions(username)
        events = save_user_events(username)
        received_events = save_received_events(username)
        total_stars = user_stars
        
        print(Fore.GREEN + Style.BRIGHT + "\n🚀 GitHub User Info:")
        print(f"{Fore.CYAN}👤 Username\n> {Fore.WHITE}{user.get('login')}")
        print(f"{Fore.LIGHTBLUE_EX}📝 Name\n> {Fore.WHITE}{user.get('name')}\n")
        print(f"{Fore.MAGENTA}🆔 ID\n> {Fore.WHITE}{user.get('id')}")
        print(f"{Fore.LIGHTYELLOW_EX}🧬 Node ID\n> {Fore.WHITE}{user.get('node_id')}\n")
        print(f"{Fore.LIGHTCYAN_EX}📧 Email\n> {Fore.WHITE}{email}")
        print(f"{Fore.RED}📍 Location\n> {Fore.WHITE}{user.get('location')}\n")
        print(f"{Fore.LIGHTBLUE_EX}🧾 Bio\n> {Fore.WHITE}{user.get('bio')}")
        print(f"{Fore.YELLOW}💼 Company\n> {Fore.WHITE}{user.get('company')}\n")
        print(f"{Fore.LIGHTBLUE_EX}🔗 Blog\n> {Fore.BLUE}{user.get('blog')}")
        print(f"{Fore.CYAN}🐦 Twitter (X)\n{Fore.BLUE}@{user.get('twitter_username')}" if user.get('twitter_username') else f"{Fore.CYAN}🐦 Twitter (X)\n> {Fore.WHITE}N/A")
        print(f"\n{Fore.YELLOW}📦 Public Repos\n> {Fore.WHITE}{user.get('public_repos')}")
        print(f"{Fore.LIGHTYELLOW_EX}📄 Public Gists\n> {Fore.WHITE}{user.get('public_gists')}\n")
        print(f"{Fore.CYAN}👥️ Followers\n> {Fore.WHITE}{user.get('followers')}")
        print(f"{Fore.LIGHTYELLOW_EX}🏷  Following\n> {Fore.WHITE}{user.get('following')}\n")
        print(f"{Fore.YELLOW}⭐ User Stars\n> {Fore.WHITE}{user_stars}")
        print(f"{Fore.LIGHTYELLOW_EX}⭐ Projet Stars\n> {Fore.WHITE}{projet_stars}\n")
        print(f"{Fore.RED}📅 Events\n> {Fore.WHITE}{events}")
        print(f"{Fore.LIGHTBLUE_EX}📃 Received Events\n> {Fore.WHITE}{received_events}\n")
        print(f"{Fore.YELLOW}🔔 Subscriptions\n> {Fore.WHITE}{len(subscriptions)} repos")
        print(f"{Fore.BLUE}🌐 Top Languages\n> {Fore.WHITE}{','.join(top_languages)}")
        print(f"{Fore.GREEN}✅ Hireable\n> {Fore.WHITE}{user.get('hireable')}\n")
        print(f"{Fore.LIGHTRED_EX}🗓️  Created At\n> {Fore.WHITE}{format_date(user.get('created_at'))}")
        print(f"{Fore.LIGHTBLUE_EX}⏱️  Updated At\n> {Fore.WHITE}{format_date(user.get('updated_at'))}\n")
        print(f"{Fore.LIGHTGREEN_EX}🖼️  Avatar URL\n{Fore.BLUE}{user.get('avatar_url')}")
        print(f"{Fore.LIGHTBLUE_EX}🔗 GitHub URL\n{Fore.BLUE}{user.get('html_url')}")
        print(Style.RESET_ALL)
        
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n💾 Saving data to files...\n")
        
        saved_files = []
        if save_user_info(username, user, name, email, total_stars, projet_stars, top_languages, events, received_events): saved_files.append("info.txt")

        followers = get_paginated_data(f"https://api.github.com/users/{username}/followers")
        if save_list_to_file(username, "followers", followers): saved_files.append("followers.txt")

        following = get_paginated_data(f"https://api.github.com/users/{username}/following")
        if save_list_to_file(username, "following", following): saved_files.append("following.txt")

        if save_repos_to_file(username, repos): saved_files.append("repos.txt")

        gists = get_paginated_data(f"https://api.github.com/users/{username}/gists")
        if save_gists_to_file(username, gists): saved_files.append("gists.txt")
        if save_user_stars(username, repos): saved_files.append("star-user.txt")
        if save_starred_projects(username): saved_files.append("star-projet.txt")
        orgs = get_user_orgs(username)
        if save_orgs_to_file(username, orgs): saved_files.append("orgs.txt")
        if save_subscriptions_to_file(username, subscriptions): saved_files.append("subscriptions.txt")
        if save_user_events(username) > 0:
            saved_files.append("events.txt")
        if save_received_events(username) > 0:
            saved_files.append("received_events.txt")
        
        if not saved_files:
            folder = f"./{username}"
            if os.path.exists(folder):
                os.rmdir(folder)

        option = input(fade.fire("\nPress Enter to search again, or type 'exit' next time to exit."))
        if option.strip().lower() == "exit":
            print(Fore.RED + Style.BRIGHT + "Exittng")
            break
            return

if __name__ == "__main__":
    main()