# Check password strength with Password_Strength module
from password_strength import PasswordPolicy

password_policy = PasswordPolicy.from_names(
	length=5,  # min length: 8
	uppercase=1,  # need min. 2 uppercase letters
	numbers=1,  # need min. 2 digits
	special=1,  # need min. 2 special characters
	nonletters=0,  # need min. 2 non-letter characters (digits, specials, anything)
)