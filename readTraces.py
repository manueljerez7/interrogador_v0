import csv
import matplotlib.pyplot as plt
from zip import zip
import os

def get_nums(lista_caracteres):
    resultado = []
    numero_actual = ""
    negativo = False

    for caracter in lista_caracteres:
        if caracter.isdigit() or caracter == '.':
            numero_actual += caracter
        elif caracter == '-':
            negativo = True
        elif caracter == ',':
            # Si hay un espacio, procesar el número actual
            if numero_actual:
                numero = float(numero_actual.replace(',', '.'))
                resultado.append(-numero if negativo else numero)
                numero_actual = ""
                negativo = False

    # Procesar el último número después del último espacio (o al final de la lista)
    if numero_actual:
        numero = float(numero_actual.replace(',', '.'))
        resultado.append(-numero if negativo else numero)

    return resultado



def gen_csv_zip(temp,ficheros_brutos):
    # Ruta del archivo
    ficheros_csv = []
    for archivo_ruta in ficheros_brutos:

        # Lista para almacenar arrays de números completos
        numeros_completos = []

        # Utilizar csv.reader para leer el archivo
        with open(archivo_ruta, newline='') as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                # Procesar cada fila para obtener un array de números completos
                valores = [valor.replace('"', '') for valor in fila[1:] if valor != '']
                numeros_completos_fila = []
                fila.remove('\n')
                cadena = "".join([str(i) for i in fila])
                numeros_completos.append(get_nums(cadena))

        # Escribir la lista de listas en el archivo CSV
        with open(archivo_ruta+'.csv', 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerows(numeros_completos)
            ficheros_csv.append(archivo_ruta+'.csv')

    #Tenemos los 4 ficheros csv y los 4 brutos. Queremos borrar los brutos y hacer un zip y borrar los csv
    zip(temp,ficheros_csv)

    # Eliminar los archivos originales después de crear el zip
    for archivo in ficheros_brutos:
        os.remove(archivo)
