import re

def validate(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9!$&\-+]+@[a-zA-Z0-9\-+]+\.[a-zA-Z]{2,}$"
    match = re.search(pattern, email)
    return match is not None