import requests
import datetime

def lookup_discord_invite_full():
    invite = input("Enter Discord invite (code or URL): ").strip()
    invite = invite.replace("https://discord.gg/", "").replace("discord.gg/", "")

    url = f"https://discord.com/api/v10/invites/{invite}?with_counts=true&with_expiration=true"

    r = requests.get(url)
    if r.status_code != 200:
        print("Invalid or expired invite")
        return

    data = r.json()
    guild = data.get("guild", {})

    print("\nDiscord Server Lookup (FULL)")
    print("=" * 70)

    print("Server name:", guild.get("name"))
    print("Server ID:", guild.get("id"))
    print("Description:", guild.get("description", "None"))

    print("Members:", data.get("approximate_member_count"))
    print("Online:", data.get("approximate_presence_count"))

    print("Verification level:", guild.get("verification_level"))
    print("NSFW level:", guild.get("nsfw_level"))

    print("Boost tier:", guild.get("premium_tier"))
    print("Boost count:", guild.get("premium_subscription_count"))

    features = guild.get("features", [])
    print("Server features (tags):", ", ".join(features) if features else "None")

    print("Vanity URL:", guild.get("vanity_url_code"))
    print("Icon hash:", guild.get("icon"))
    print("Banner hash:", guild.get("banner"))
    print("Splash hash:", guild.get("splash"))

    expires = data.get("expires_at")
    if expires:
        expires = datetime.datetime.fromisoformat(expires.replace("Z", ""))
    print("Invite expires at:", expires if expires else "Never")

    print("Temporary invite:", data.get("temporary", False))

    print("=" * 70)

if __name__ == "__main__":
    lookup_discord_invite_full()
