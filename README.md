# interrogador_v0
Repositorio para la lectura automatizada del interrogador óptico HBM BraggMETER.

**Ejecución:**
_test_socket.py [-h] -c CONFIG_FILE -s SAMPLES -t TEMPERATURE -l LOG_FILE_

Genera una carpeta comprimida XX.X.zip donde XX.X es la temperatura de la medida

Ficheros:
- test_socket.py - Fichero para ejecución de medidas en interrogador óptico
- readTraces.py - Funciones de apoyo para la conversión de ficheros generados por el interrogador a csv adecuado para la lectura y compresión
