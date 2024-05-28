import threading
import socket

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '0.0.0.0'  # Escuchar en todas las interfaces de red disponibles
TCP_PORT = 12345
BUFFER_SIZE = 1024
MESSAGE_DELIMITER = b'\n'

clientes = {}  # Diccionario para almacenar las conexiones de clientes

def broadcast(message, source_conn):
    """Envía un mensaje a todos los clientes conectados excepto al remitente."""
    for conn in clientes.values():
        if conn != source_conn:
            conn.sendall(message)

def contacto_cliente(conn, addr):
    """Maneja la comunicación con un cliente."""
    print(f"[SERVIDOR] Conectado satisfactoriamente con {addr}")
    clientes[addr] = conn
    print(f"[SERVIDOR] Clientes conectados: {len(clientes)}")