import sqlite3

def inicializar_bdd():
    try:
        conexion = sqlite3.connect('eventos.db')
        cursor = conexion.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS mensajes_cli (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       contenido TEXT NOT NULL,
                       fecha_envio TEXT NOT NULL,
                       ip_cliente TEXT NOT NULL)
                       ''')
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        print(f'No se pudo crear la base de daros. Error: {e}')
        return False

def registrar_mensaje_cli(contenido, fecha_envio, ip_cliente):
    try:
        conexion = sqlite3.connect('eventos.db')  
        cursor = conexion.cursor()
        cursor.execute('''
                       INSERT INTO mensajes_cli (contenido, fecha_envio, ip_cliente)
                       VALUES (?, ?, ?)
                       ''', (contenido, fecha_envio, ip_cliente))
        conexion.commit() 
        conexion.close()   
    except sqlite3.Error as e:
        print(f"Error al guardar mensaje del cliente: {e}")
