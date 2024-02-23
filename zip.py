import zipfile
import os

def zip(nombre_zip,archivos_a_zippear):
    # Crear el archivo zip
    nombre=nombre_zip+".zip"
    with zipfile.ZipFile(nombre, 'w') as zip_file:
        for archivo in archivos_a_zippear:
            # Añadir cada archivo al zip
            zip_file.write(archivo)

    # Eliminar los archivos originales después de crear el zip
    for archivo in archivos_a_zippear:
        os.remove(archivo)
