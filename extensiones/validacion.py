import re
def validar_soloString(dato):
    regex = r"^\w{3,15}$"
    if re.match(regex,dato):
        return True
    else:

        return False
def validar_numCelular(numero):
    regex = r"/^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$/" #puede llevar o no +56 pero debe llevar 9
    if re.match(regex,numero):
        return True
    else:

        return False

def validar_int(dato):
    try:
        int(dato)
        return True
    except(ValueError):
        return False

def validar_rut(rut):
    regex = r'^(\d{1,2}(?:[\.]?\d{3}){2}-[\dkK])$'

    if re.match(regex, rut):
        return True
    else:

        return False

def validar_email(email):
    regex = r"^(?i)[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$" #ya lo hace html anyways
    #"^(?i)[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$" regex mas 
    #r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'#uno corto y simple
    if re.match(regex, email):
        return True
    else:
        return False
    

"""

validacion=True

string="sas"
email="enzo@hotmail.es"
rut="20915611-3"
numero="1"

if validar_soloString(string)==False:
    validacion=False
if validar_email(email)==False:
    validacion=False
if validar_rut(rut)==False:
    validacion=False
if validar_int(numero)==False:
    validacion=False
if validacion==True:
    print("token")
else:
    print("Complete las casillas segun lo pedido")
"""
