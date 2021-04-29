import sqlite3
from sqlite3 import Error

try:
    with sqlite3.connect("Ventas.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Venta (Folio INTEGER PRIMARY KEY AUTOINCREMENT, Nombre TEXT NOT NULL);")
        c.execute("CREATE TABLE IF NOT EXISTS DetalleVenta (IDdetalle INTEGER PRIMARY KEY,Folio KEY ,Fecha timestamp NOT NULL, Producto TEXT NOT NULL, Cantidad INTEGER NOT NULL, Precio INTEGER NOT NULL,FOREIGN KEY(Folio) REFERENCES venta(Folio));")


except Error as e:
    print (e)
except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    conn.close()