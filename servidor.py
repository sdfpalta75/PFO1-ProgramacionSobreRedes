import socket
import threading
import datetime

HOST = '127.0.0.1'      # localhost
PUERTO = 5000         # puerto de escucha

def inicializar_socket_servidor():
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # se crea objeto socket con direcciones IPv4, tipo TCP
        servidor.bind((HOST, PUERTO))           # se asocia el socket a la direccion del servidor y puerto de escucha
        servidor.listen()           # socket en escucha
        print(f'Servidor escuchando en {HOST}:{PUERTO}')
        return servidor            # retorna el objeto configurado
    except socket.error as e:
        print(f'Error al crear el socket servidor: {e}')
        return 'error'

def aceptar_conexion(servidor):      # se acepta conexion con cliente y se le asigna un hilo, aprovechando concurrencia
    while True:
        socket_cliente, direccion = servidor.accept()
        print(f'Conexión aceptada {direccion}')
        hilo = threading.Thread(target=recibir_mensaje, args=(socket_cliente, direccion))
        hilo.start()

def recibir_mensaje(socket_cliente, direccion):
    try:
        while True:
            mensaje = socket_cliente.recv(1024).decode()
            if not mensaje:
                break
            momento = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'Mensaje de {direccion}, recibido {momento}: {mensaje}')
            respuesta = f'Mensaje recibido {momento}'
            socket_cliente.sendall(respuesta.encode())
    except socket.error as e:
        print(f'Error en la conexión con {direccion}: {e}')
    finally:
        socket_cliente.close()
        print(f'Se cerró conexión con {direccion}')


if __name__ == '__main__':
    conexion_servidor = inicializar_socket_servidor()
    if conexion_servidor == 'error':
        print('No se pudo inicializar el servidor')
    else:
        aceptar_conexion(conexion_servidor)