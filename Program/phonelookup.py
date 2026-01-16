import phonenumbers
from phonenumbers import (
    geocoder,
    carrier,
    timezone,
    number_type,
    is_valid_number,
    is_possible_number,
    region_code_for_number,
    PhoneNumberFormat
)

def lookup_phone_number():
    phone_input = input("Enter a phone number : ")

    try:
        phone_number = phonenumbers.parse(phone_input, None)

        print("\nPhone Number Analysis")
        print("=" * 50)

        print("E.164 format:",
              phonenumbers.format_number(phone_number, PhoneNumberFormat.E164))
        print("International format:",
              phonenumbers.format_number(phone_number, PhoneNumberFormat.INTERNATIONAL))
        print("National format:",
              phonenumbers.format_number(phone_number, PhoneNumberFormat.NATIONAL))

        region = region_code_for_number(phone_number)
        print("Region code:", region)
        print("Country calling code:", phone_number.country_code)
        print("Country name:",
              geocoder.description_for_number(phone_number, "en"))

        carrier_name = carrier.name_for_number(phone_number, "en")
        print("Carrier:", carrier_name if carrier_name else "Unknown")

        print("Time zone(s):",
              ", ".join(timezone.time_zones_for_number(phone_number)))

        line_type = number_type(phone_number)
        line_types = {
            0: "Fixed line",
            1: "Mobile",
            2: "Fixed or mobile",
            3: "Toll-free",
            4: "Premium rate",
            5: "Shared cost",
            6: "VoIP",
            7: "Personal number",
            8: "Pager",
            9: "UAN",
            10: "Unknown"
        }

        line_type_name = line_types.get(line_type, "Unknown")
        print("Line type:", line_type_name)

        print("Geographic number:", line_type in (0, 2))

        print("Valid number:", is_valid_number(phone_number))
        print("Possible number:", is_possible_number(phone_number))

        national_number = str(phone_number.national_number)
        print("National number length:", len(national_number))

        print("=" * 50)

    except phonenumbers.NumberParseException as e:
        print("Parsing error:", e)

if __name__ == "__main__":
    lookup_phone_number()
