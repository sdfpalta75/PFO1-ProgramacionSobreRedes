import socket
import threading
import datetime
import time
import bdd

HOST = '127.0.0.1'      # localhost
PUERTO = 5000         # puerto de escucha
clientes_activos = 0
servidor_activo = True
candado = threading.Lock()

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
    global clientes_activos
    while servidor_activo:
        try:
            servidor.settimeout(1.0)      # permite que el flujo no quede bloqueado indefinidamente por accept()
            socket_cliente, direccion = servidor.accept()
            print(f'Conexión aceptada {direccion}')
            with candado:
                clientes_activos += 1
            hilo = threading.Thread(target=recibir_mensaje, args=(socket_cliente, direccion))
            hilo.daemon = True        # permite que el hilo se cierre al finalizar el programa
            hilo.start()
        except socket.timeout:
            continue
        except socket.error as e:
            if servidor_activo:
                print(f'Error de conexión: {e}')
            break

def recibir_mensaje(socket_cliente, direccion):
    global clientes_activos, servidor_activo
    try:
        while True:
            mensaje = socket_cliente.recv(1024).decode()
            if not mensaje:
                break
            momento = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'Mensaje de {direccion}, recibido {momento}: {mensaje}')
            respuesta = f'Mensaje recibido {momento}'
            with candado:
                bdd.registrar_mensaje_cli(mensaje, momento, direccion[0])    # registra en la bdd
            socket_cliente.sendall(respuesta.encode())
    except socket.error as e:
        print(f'Error en la conexión con {direccion}: {e}')
    finally:
        socket_cliente.close()
        print(f'Se cerró conexión con {direccion}')
        with candado:
            clientes_activos -= 1        # actualiza el contador de clientes
            if clientes_activos == 0:    # si no hay más clientes, cambia estado de servidor_activo
                servidor_activo = False

if __name__ == '__main__':
    if not bdd.inicializar_bdd():     # fuerza la creacion de la bdd. devuelve True si es correcta o Falsi, si hubo algún error
        print('No se pudo inicializar la base de datos. Servidor cerrado')
    else:
        conexion_servidor = inicializar_socket_servidor()
        if conexion_servidor == 'error':
            print('No se pudo inicializar el servidor')
        else:
            hilo_aceptador = threading.Thread(target=aceptar_conexion, args=(conexion_servidor,))
            hilo_aceptador.daemon = True
            hilo_aceptador.start()
            while servidor_activo:      # se mantiene mientras que sea True, cuando cambia el estado ejecuta el cierre del socket del servidor
                time.sleep(1)        
            print('Cerrando el servidor')
            conexion_servidor.close()
            print('Servidor cerrado')