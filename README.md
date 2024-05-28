# Servidor y Cliente TCP Concurrente

Este proyecto implementa un servidor y un cliente TCP concurrente en Python. El servidor acepta múltiples conexiones de clientes y permite la comunicación bidireccional. Además, los clientes pueden enviar mensajes que serán difundidos a todos los demás clientes conectados usando #.

## Requisitos

- Python 3.x

## Uso

### Servidor

1. Ejecuta el servidor:
    
    python servidor.py
    
   El servidor comenzará a escuchar en el puerto `12345`.

### Cliente

1. Ejecuta el cliente:
    
    python cliente.py [IP_DEL_SERVIDOR]
    
   - `IP_DEL_SERVIDOR` (opcional): La dirección IP del servidor al que desea conectar. Por defecto es `127.0.0.1`.

2. Después de conectarse, el cliente puede enviar mensajes escribiéndolos directamente en la consola.

## Funcionalidades

- El servidor imprime la dirección del cliente y la cantidad de clientes conectados.
- El cliente imprime "Conectado satisfactoriamente" al establecer la conexión.
- Los mensajes enviados por el cliente se muestran en el servidor.
- Los mensajes enviados por el servidor se muestran en el cliente.
- Si un mensaje enviado por el cliente comienza con `#`, el servidor lo difunde a todos los demás clientes.
- Al recibir el mensaje `logout`, la conexión se cierra en ambos lados.
