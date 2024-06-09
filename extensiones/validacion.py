import re
def validar_soloString(dato):
    regex = r'[a-zA-Z]{3,}'
    if dato=="":
        return False
    if re.match(regex,dato):
        return True
    else:

        return False
def validar_numCelular(numero):
    regex = r"^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$"#puede llevar o no +56 pero debe llevar 9 y el total de digitos debe ser 7 (sin contar  56)

    if re.match(regex,numero):
        return True
    else:
        return False

def validar_int(dato):
    try:
        valor = int(dato)
        if valor=="":
            return False
        if valor >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


def validar_rut(rut):
    regex = r'^[1-9]\d*\-(\d|k|K)$' #debe llevar guion

    if re.match(regex, rut):
        return True
    else:

        return False

def validar_email(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' #ya lo hace html anyways
    #"^(?i)[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$" regex mas 
    #r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'#uno corto y simple
    if re.match(regex, email):
        return True
    else:
        return False

    
    
def validar_depto(dato):
    regex = r'^[a-zA-Z0-9]+$'
    if dato=="":
        return True
    if re.match(regex,dato):
        return True
    else:

        return False
    
    
def validar_piso(dato):
    try:
        # Si dato está vacío, considerarlo válido
        if dato == "":
            return True
        # Intenta convertir dato a un entero
        valor = int(dato)
        # Si valor es un entero, es válido
        return True
    except ValueError:
        # Si ocurre un ValueError, dato no es un entero válido
        return False

def validar_calle(dato):
    regex = r'[a-zA-Z\s]{3,}'
    # Si el dato está vacío, no es válido
    if dato == "":
        return False
    # Verifica si el dato coincide con el patrón
    return bool(re.match(regex, dato))