import socket

HOST = '127.0.0.1'
PUERTO = 5000

def inicializar_cliente():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PUERTO))
        print(f'Se estableció conexión con el servidor en {HOST}:{PUERTO}')
        while True:
            mensaje = input('Escriba un mensaje ("éxito" para salir): ')
            if mensaje == '':
                print('Mensaje vacío. Intente nuevamente.')
                continue
            if mensaje.lower() in ('éxito', 'exito'):
                break
            cliente.sendall(mensaje.encode())
            respuesta = cliente.recv(1024).decode()
            print(f'Respuesta del servidor: {respuesta}')
        cliente.close()
        print('Se cerró la conexión correctamente.')
    except socket.error as e:
        print(f'Error de conexión: {e}')

if __name__ == '__main__':
    inicializar_cliente()