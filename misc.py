import re
import string
import random 

def email_validation(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}.+[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

def email_code():
   return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def generate_license():
   def license_part():
      license = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
      return license
   license = f"{license_part()}-{license_part()}-{license_part()}-{license_part()}"
   return license

def random_id():
   id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
   return id

def validate_password(password: string):
   if set(password).difference(string.ascii_letters + string.digits): 
      for charecter in password:
         charecter = str(charecter)
         if charecter.isupper():
            return True 
         else:
            return False    
   else:
      return False          