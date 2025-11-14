import re

def validate(password: str) -> bool:
    if len(password) < 8:
        return False
    
    capital_letter = "[A-Z]+"
    if re.search(capital_letter, password) is None:
        return False
    
    small_letter = "[a-z]+"
    if re.search(small_letter, password) is None:
        return False
    
    number = "[0-9]+"
    if re.search(number, password) is None:
        return False
    
    special = "\\W+"
    if re.search(special, password) is None:
        return False

    return True