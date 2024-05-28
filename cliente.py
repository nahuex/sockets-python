import sys
import socket
import threading

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024
MESSAGE_DELIMITER = b'\n'

# Permitir pasar la IP del servidor como argumento
if len(sys.argv) >= 2:
    TCP_IP = sys.argv[1]

def recibir_mensajes(sock):
    """Recibe mensajes del servidor y los imprime"""
    while True:
        try:
            data = bytearray()
            while True:
                recvd = sock.recv(BUFFER_SIZE)
                if not recvd:
                    break
                data += recvd
                if MESSAGE_DELIMITER in recvd:
                    msg = data.rstrip(MESSAGE_DELIMITER).decode('utf-8')
                    print(f"[CLIENTE] Mensaje Recibido: {msg}")
                    if msg.lower() == "logout":
                        print("[CLIENTE] Desconectando del Servidor")
                        sock.close()
                        return
                    data.clear()
        except ConnectionError:
            print("[CLIENTE] Error de conexión")
            break
        except Exception as e:
            print(f"[CLIENTE] Error inesperado: {e}")
            break    