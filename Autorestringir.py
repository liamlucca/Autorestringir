import time
import requests
from cryptography.fernet import Fernet
import os
from datetime import datetime

# Clave para cifrar/descifrar (generada una vez y embebida en el ejecutable)
KEY = b''  # Reemplazar con una clave generada por Fernet.generate_key()
cipher = Fernet(KEY)

# Días permitidos para desencriptar
decryptedDays = [5,6]  # 0 = lunes, 1 = martes, 2 = miercoles, 3 = jueves, 4 = viernes, 5 = sabado, 6 = domingo

# Hora mínima para desencriptar (en UTC, formato 24h, por ejemplo, 12 para 12:00 pm UTC)
DECRYPTION_START_HOUR = 12  # Cambia esto a la hora que quieras (por ejemplo, 14 para 2:00 pm UTC)

# Nombres de los archivos
INFO_FILE = "info.txt"  # Archivo inicial con la contraseña (no encriptado)
ENCRYPTED_INFO_FILE = "info_encriptada.txt"  # Archivo con contenido encriptado
DECRYPTED_INFO_FILE = "info_desencriptada.txt"  # Archivo con contenido desencriptado

# APIs para obtener la fecha (en orden de prioridad)
API_ENDPOINTS = [
    {"url": "http://worldtimeapi.org/api/timezone/Etc/UTC", "key": None, "format": "worldtime"},
    {"url": "http://worldclockapi.com/api/json/utc/now", "key": None, "format": "worldclock"},
    #{"url": "http://api.timezonedb.com/v2.1/get-time-zone?key=[INSERT_KEY_HERE]&format=json&by=zone&zone=UTC", "key": "[INSERT_KEY_HERE]", "format": "timezonedb"},
]

# Función para obtener la fecha y hora real desde múltiples APIs
def get_current_day_and_hour():
    max_retries = 3
    for api in API_ENDPOINTS:
        for attempt in range(max_retries):
            try:
                response = requests.get(api["url"], timeout=5)
                response.raise_for_status()
                data = response.json()
                
                if api["format"] == "worldtime":
                    dt = datetime.fromisoformat(data["datetime"].replace("Z", "+00:00"))
                    current_day = dt.weekday()
                    current_hour = dt.hour
                elif api["format"] == "timezonedb":
                    dt = datetime.strptime(data["formatted"], "%Y-%m-%d %H:%M:%S")
                    current_day = dt.weekday()
                    current_hour = dt.hour
                elif api["format"] == "worldclock":
                    dt = datetime.strptime(data["currentDateTime"], "%Y-%m-%dT%H:%M%z")
                    current_day = dt.weekday()
                    current_hour = dt.hour
                
                return current_day, current_hour
            except requests.RequestException as e:
                print(f"Intento {attempt + 1}/{max_retries} falló para {api['url']}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Esperar 2 segundos antes de reintentar
                continue
    return None, None  # Si todas las APIs fallan, denegar acceso

# Función para encriptar info.txt y crear info_encriptada.txt (si no existe)
def encrypt_info_file():
    if os.path.exists(INFO_FILE) and not os.path.exists(ENCRYPTED_INFO_FILE):
        try:
            with open(INFO_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            encrypted_content = cipher.encrypt(content.encode())
            with open(ENCRYPTED_INFO_FILE, "wb") as f:
                f.write(encrypted_content)
            print(f"Archivo {ENCRYPTED_INFO_FILE} creado con el contenido encriptado.")
        except Exception as e:
            print(f"Error al encriptar {INFO_FILE}: {e}")
    elif os.path.exists(ENCRYPTED_INFO_FILE):
        print(f"El archivo {ENCRYPTED_INFO_FILE} ya existe, no se reemplaza.")
    else:
        print(f"No se encontró {INFO_FILE}. Crea el archivo con tu contraseña primero.")

# Función para desencriptar info_encriptada.txt si es día permitido y después de la hora configurada
def decrypt_info_file():
    current_day, current_hour = get_current_day_and_hour()
    if current_day is None or current_hour is None:
        return "Error: No se pudo verificar la fecha. Necesitas conexión a internet."
    if current_day in decryptedDays and current_hour >= DECRYPTION_START_HOUR:
        if os.path.exists(ENCRYPTED_INFO_FILE) and not os.path.exists(DECRYPTED_INFO_FILE):
            try:
                with open(ENCRYPTED_INFO_FILE, "rb") as f:
                    encrypted_content = f.read()
                decrypted_content = cipher.decrypt(encrypted_content).decode()
                with open(DECRYPTED_INFO_FILE, "w", encoding="utf-8") as f:
                    f.write(decrypted_content)
                return f"Archivo {DECRYPTED_INFO_FILE} creado con el contenido desencriptado."
            except Exception as e:
                return f"Error al desencriptar {ENCRYPTED_INFO_FILE}: {e}"
        elif os.path.exists(DECRYPTED_INFO_FILE):
            return f"El archivo {DECRYPTED_INFO_FILE} ya existe, no se reemplaza."
        else:
            return f"No se encontró {ENCRYPTED_INFO_FILE}. Crea el archivo encriptado primero."
    else:
        if current_day not in decryptedDays:
            return f"Acceso denegado: Solo puedes desencriptar los días: {printDecryptedDays()}"
        else:
            return f"Acceso denegado: Solo puedes desencriptar después de las {DECRYPTION_START_HOUR}:00 UTC."

# Función para mostrar los días permitidos
def printDecryptedDays():
    daysToPrint = ""
    for day in decryptedDays:
        match day:
            case 0: daysToPrint += "Lunes "
            case 1: daysToPrint += "Martes "
            case 2: daysToPrint += "Miércoles "
            case 3: daysToPrint += "Jueves "
            case 4: daysToPrint += "Viernes "
            case 5: daysToPrint += "Sábado "
            case 6: daysToPrint += "Domingo "
    return daysToPrint

# Programa principal
def main():
    # Manejo de info.txt
    encrypt_info_file()
    print(decrypt_info_file())

if __name__ == "__main__":
    main()

input("Presionar Enter para salir")