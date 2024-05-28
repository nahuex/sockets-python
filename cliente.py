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
                recvd = sock.recv(BUFFER_SIZE) #Recibir datos del servidor.
                if not recvd:
                    break
                data += recvd
                if MESSAGE_DELIMITER in recvd:
                    msg = data.rstrip(MESSAGE_DELIMITER).decode('utf-8')
                    print(f"[CLIENTE] Mensaje Recibido: {msg}")
                    if msg.lower() == "logout": #Finalizar la conexión si se recibe logout.
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

def iniciar_cliente():
    """Inicia el Cliente TCP"""
    print("[CLIENTE] Iniciando")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("[CLIENTE] Conectando")
        s.connect((TCP_IP, TCP_PORT)) #Conectarse al servidor.
        print(f"[CLIENTE] Conectado satisfactoriamente a {TCP_IP}:{TCP_PORT}")

        receiver_thread = threading.Thread(target=recibir_mensajes, args=(s,), daemon=True)
        receiver_thread.start() #Iniciar un hilo para recibir mensajes.

        while True:
            msg = input() #Leer entrada del usuario y enviarla al servidor.
            if msg.lower() == "logout": #Enviar logout y terminar la conexión.
                s.sendall((msg + '\n').encode('utf-8'))
                break
            s.sendall((msg + '\n').encode('utf-8'))

if __name__ == "__main__":
    iniciar_cliente()