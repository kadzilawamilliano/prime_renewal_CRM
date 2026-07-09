import re

def clean_phone(phone):

    phone = re.sub(r"\D", "", str(phone))

    if phone.startswith("265"):
        international = phone
        local = "0" + phone[3:]

    elif phone.startswith("0"):
        local = phone
        international = "265" + phone[1:]

    else:
        local = phone
        international = phone

    return local, international
