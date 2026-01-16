import dns.resolver
from email_validator import validate_email, EmailNotValidError

PROVIDERS = {
    "gmail.com": {
        "name": "Google Gmail",
        "type": "Public email provider",
        "company": "Google LLC",
    },
    "outlook.com": {
        "name": "Microsoft Outlook",
        "type": "Public email provider",
        "company": "Microsoft",
    },
    "hotmail.com": {
        "name": "Microsoft Hotmail",
        "type": "Public email provider",
        "company": "Microsoft",
    },
    "live.com": {
        "name": "Microsoft Live Mail",
        "type": "Public email provider",
        "company": "Microsoft",
    },
    "yahoo.com": {
        "name": "Yahoo Mail",
        "type": "Public email provider",
        "company": "Yahoo",
    },
    "proton.me": {
        "name": "Proton Mail",
        "type": "Privacy-focused provider",
        "company": "Proton AG",
    },
    "protonmail.com": {
        "name": "Proton Mail",
        "type": "Privacy-focused provider",
        "company": "Proton AG",
    }
}

DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "10minutemail.com",
    "guerrillamail.com",
    "yopmail.com",
    "tempmail.com"
}

def lookup_email():
    email_input = input("Enter an email address: ").strip()

    print("\nEmail Provider Lookup")
    print("=" * 50)

    try:
        valid = validate_email(email_input)
        email = valid.email
        print("Valid email format: True")
    except EmailNotValidError as e:
        print("Valid email format: False")
        print("Error:", e)
        return

    local_part, domain = email.split("@")

    print("Email:", email)
    print("Local part:", local_part)
    print("Domain:", domain)

    provider = PROVIDERS.get(domain.lower())

    if provider:
        print("Provider:", provider["name"])
        print("Provider type:", provider["type"])
        print("Company:", provider["company"])
        print("Custom domain:", False)
    else:
        print("Provider: Custom or unknown domain")
        print("Provider type: Custom domain")
        print("Custom domain:", True)

    print("Disposable email:", domain.lower() in DISPOSABLE_DOMAINS)

    try:
        mx_records = dns.resolver.resolve(domain, "MX")
        mx_hosts = [r.exchange.to_text() for r in mx_records]
        print("MX servers:", ", ".join(mx_hosts))

        if any("google" in mx.lower() for mx in mx_hosts):
            print("Mail infrastructure: Google")
        elif any("outlook" in mx.lower() or "microsoft" in mx.lower() for mx in mx_hosts):
            print("Mail infrastructure: Microsoft")
        elif any("proton" in mx.lower() for mx in mx_hosts):
            print("Mail infrastructure: Proton")
        else:
            print("Mail infrastructure: Unknown")
    except Exception:
        print("MX servers: Not found")

    print("=" * 50)

if __name__ == "__main__":
    lookup_email()
