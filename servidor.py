import threading
import socket

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '0.0.0.0'  # Escuchar en todas las interfaces de red disponibles
TCP_PORT = 12345
BUFFER_SIZE = 1024
MESSAGE_DELIMITER = b'\n'