import sys
import socket
import threading

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024
MESSAGE_DELIMITER = b'\n'