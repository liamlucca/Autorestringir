# Autorestringir
Para encriptar archivos de texto y desbloquearlos los dias de las semana seleccionados (por ejemplo: sabados y domingos). Fue creado para guardar las contraseñas de las redes sociales durante la semana y no procrastinar.

## Importante
### Requisitos 
- Python 3.10+
- Librerias: cryptography, pyinstaller
### Instrucciones
1. Cambiar las constantes `decryptedDays` y `DECRYPTION_START_HOUR` para configurar los días y hora permitidos para desencriptar.
2. Copiar la clave que se obtiene con ejecutar las siguientes lineas de código en Python:
```
from cryptography.fernet import Fernet
print(Fernet.generate_key())
```
3. Ir a `Autorestringir.py` y pegar la clave en la constante `KEY`.
4. Correr el siguiente comando `pyinstaller --onefile Autorestringir.py` para transformar el archivo de python en un ejecutable.
5. Crear un archivo llamado `info.txt` y guardar lo que se quiera encriptar o proteger.
6. Ejecutar el `Autorestringir.exe` (generado en el paso 4).
7. Si se generó `info_encriptada.txt`, la información está encriptada y ya se pueden eliminar los archivos `info.txt` y `Autorestringir.py`.
8. Para desencriptar el archivo `info_encriptada.txt` se debe esperar al día y hora establecidos (en el paso 1) y volver a ejecutar `Autorestringir.exe`.
