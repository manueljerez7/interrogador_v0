import csv
import matplotlib.pyplot as plt

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


# Ruta del archivo
archivo_ruta = '23.0_temp'  # Reemplaza con la ruta correcta de tu archivo

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

arrays_canales = []

for i in range(len(numeros_completos[0])):
    # Crear una nueva lista para la posición i
    nueva_lista = [sublista[i] for sublista in numeros_completos]
    arrays_canales.append(nueva_lista)

plt.plot(arrays_canales[0])
plt.plot(arrays_canales[1])
plt.show()