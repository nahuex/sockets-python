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

    with conn:
        data = bytearray()
        while True:
            try:
                received = conn.recv(BUFFER_SIZE)
                if not received:
                    break
                data += received
                if MESSAGE_DELIMITER in received:
                    msg = data.rstrip(MESSAGE_DELIMITER).decode('utf-8')
                    print(f"[SERVIDOR] Mensaje de {addr}: {msg}")
                    if msg.lower() == "logout":
                        break
                    if msg.startswith('#'):
                        broadcast(data, conn)
                    else:
                        conn.sendall(data)  # Eco
                    data.clear()
            except ConnectionError:
                break
            except Exception as error:
                print(f"[SERVIDOR] Error: {error}")
                break
    print(f"[SERVIDOR] Desconectando {addr}")
    del clientes[addr]
    print(f"[SERVIDOR] Clientes conectados: {len(clientes)}")

def iniciar_servidor():
    """Inicia el Servidor TCP"""
    print("[SERVIDOR] Iniciando")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TCP_IP, TCP_PORT))
        s.listen()
        print(f"[SERVIDOR] Escuchando en {TCP_PORT}")
        while True:
            conn, addr = s.accept()
            print(f"[SERVIDOR] Nueva conexión de {addr}")
            thread = threading.Thread(target=contacto_cliente, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    iniciar_servidor()