# Check password strength with Password_Strength module
from password_strength import PasswordPolicy
from random import randint

passwordPolicy = PasswordPolicy.from_names(
    length=5,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
    special=1,  # need min. 2 special characters
    nonletters=0,  # need min. 2 non-letter characters (digits, specials, anything)
)

def GenerateAccount():
    res = ""
    for i in range(14):
        if i == 3 or i == 7:
            res += '-'
            continue
        res += chr(ord('0') + randint(0,9))

    return res