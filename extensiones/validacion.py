import re

def validar_rut(rut):
    
    regex = r'^(\d{1,2}(?:[\.]?\d{3}){2}-[\dkK])$'

    if re.match(regex, rut):

        return True

    else:

        return False
    
    
def validar_email(email):

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    if re.match(regex, email):

        return True

    else:

        return False
    
