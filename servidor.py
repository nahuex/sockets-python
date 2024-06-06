#Se importan las librerías threading para manejar múltiples hilos y socket para la comunicación de red.
import threading
import socket

# Configuración de la dirección IP y puerto del servidor
TCP_IP = '0.0.0.0'  # Escuchar en todas las interfaces de red disponibles
TCP_PORT = 1234 # El puerto donde el servidor escuchará las conexiones entrantes.
BUFFER_SIZE = 1024 # Tamaño del buffer para la recepción de datos.
MESSAGE_DELIMITER = b'\n' # Delimitador de mensajes para distinguir mensajes separados (en este caso, un salto de línea).

clientes = {}  # Diccionario para almacenar las conexiones de clientes

def broadcast(message, source_conn):
    """Envía un mensaje a todos los clientes conectados excepto al remitente."""
    for conn in clientes.values():
        if conn != source_conn:
            conn.sendall(message)

def contacto_cliente(conn, addr):
    """Maneja la comunicación con un cliente."""
    print(f"[SERVIDOR] Conectado satisfactoriamente con {addr}")
    clientes[addr] = conn #Añadir el cliente al diccionario. # Conexión con el cliente.
    print(f"[SERVIDOR] Clientes conectados: {len(clientes)}") #Imprime un mensaje indicando que se ha conectado un nuevo cliente y lo añade al diccionario de clientes.

    with conn:
        data = bytearray() # Almacena los datos recibidos del cliente.
        while True:
            try:
                received = conn.recv(BUFFER_SIZE) #Recibir datos del cliente.
                if not received: # Si no se reciben datos, se cierra la conexión.
                    break
                data += received
                if MESSAGE_DELIMITER in received: # Si se recibe el delimitador de mensaje, se procesa el mensaje completo.
                    msg = data.rstrip(MESSAGE_DELIMITER).decode('utf-8')
                    print(f"[SERVIDOR] Mensaje de {addr}: {msg}")
                    if msg.lower() == "logout": #Finalizar la conexión si el cliente envía logout.
                        break
                    if msg.startswith('#'): #Difundir el mensaje a todos los clientes si empieza con #.
                        broadcast(data, conn)
                    else:
                        conn.sendall(data)  #Si no, se envía un eco del mensaje de vuelta al cliente.
                    data.clear() # Limpia el buffer de datos para recibir el próximo mensaje.
            except ConnectionError:
                break
            except Exception as error:
                print(f"[SERVIDOR] Error: {error}")
                break
    print(f"[SERVIDOR] Desconectando {addr}")
    del clientes[addr] #Remover el cliente del diccionario al desconectarse.
    print(f"[SERVIDOR] Clientes conectados: {len(clientes)}")

def iniciar_servidor():
    """Inicia el Servidor TCP"""
    print("[SERVIDOR] Iniciando")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TCP_IP, TCP_PORT)) #Enlazar el socket a la dirección IP y puerto.
        s.listen() #Escuchar conexiones entrantes.
        print(f"[SERVIDOR] Escuchando en {TCP_PORT}")
        while True: # Bucle para aceptar nuevas conexiones.
            conn, addr = s.accept() #Aceptar una nueva conexión y crear un hilo para manejarla.
            print(f"[SERVIDOR] Nueva conexión de {addr}")
            thread = threading.Thread(target=contacto_cliente, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__": # Si el script se ejecuta directamente, se llama a iniciar_servidor para iniciar el servidor.
    iniciar_servidor()