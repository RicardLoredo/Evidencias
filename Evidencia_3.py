import sys
import datetime
import sqlite3
import pandas as pd
from sqlite3 import Error

try:
    with sqlite3.connect("Ventas.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        c = conn.cursor()
        fecha_actual=datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
        registros_detalle={"Fecha":fecha_actual,"Producto":None,"Cantidad":None,"Precio":None,"Folio":None}
        registro_venta={"Nombre":None}
        while (True):
            respuesta = 1
            print("\nMENU PRINCIPAL\n")
            print("[1] Registrar Venta" )
            print("[2] Consultar Venta")
            print("[3] Reporte de Ventas")
            print("[4] Salir")
            opcion_elegida = int(input("¿Qué deseas hacer?  > "))
            if opcion_elegida == 4:
                print("GRACIAS POR UTILIZAR EL PROGRAMA")
                break
            elif opcion_elegida == 1:
                nombre = input("\nDame el nombre del cliente: ")
                registro_venta["Nombre"]=nombre
                c.execute("INSERT INTO Venta (Nombre) VALUES(:Nombre)", registro_venta)
                conn.commit()
                c.execute("SELECT MAX(FOLIO) FROM Venta")
                folio = c.fetchall()[0][0]
                registros_detalle["Folio"] = folio
                while respuesta == 1:
                    producto = input("Dime la descripcion del articulo: ")
                    while True:
                        try:
                            cantidad = int(input("Dime la cantidad de piezas: "))
                            precio = str(input("Dame el precio de venta: "))
                            break
                        except ValueError:
                            print("Solo se aceptan numeros")
                            continue   
                    registros_detalle["Producto"] = producto
                    registros_detalle["Cantidad"] = cantidad
                    registros_detalle["Precio"] = precio
                    c.execute("INSERT INTO DetalleVenta (Folio,Fecha,Producto,Cantidad,Precio) VALUES(:Folio,:Fecha, :Producto, :Cantidad, :Precio)", registros_detalle)
                    conn.commit()  
                    respuesta = int(input("\n ¿Deseas capturar otro registro? \n(1-Si / 0-No): "))
                    if respuesta == 0:
                        c.execute("SELECT SUM(PRECIO) FROM DetalleVenta WHERE FOLIO = :Folio", registros_detalle)
                        precio = c.fetchall()[0][0]
                        precio = str(round(precio, 2))
                        print(f"El total a pagar del Cliente {nombre} con el Folio #{folio} es de ${precio}")
            elif opcion_elegida == 2:
                folio_buscar = int(input("\nDame el folio del cliente para consultar su venta: "))
                folio_valor = {"folio_buscar":folio_buscar}
                c.execute("SELECT D.Fecha,D.Folio,V.Nombre,D.Producto,D.Cantidad,D.Precio FROM Venta V,DetalleVenta D WHERE V.Folio = :folio_buscar AND D.Folio = :folio_buscar",folio_valor)
                folio_buscado=c.fetchall()
                c.execute("SELECT SUM(PRECIO) FROM DetalleVenta WHERE FOLIO = :folio_buscar", folio_valor)
                folio_precio = c.fetchall()[0][0]
                if folio_precio == None:
                    pass
                else:
                    folio_precio = str(round(folio_precio, 2))
                c.execute("SELECT V.Nombre,D.Folio FROM Venta V,DetalleVenta D WHERE V.Folio = :folio_buscar AND D.Folio = :folio_buscar",folio_valor)
                folio_nombre=(c.fetchone(),)[0]
                if folio_nombre == None:
                    pass
                if folio_buscado:
                    df=pd.DataFrame(folio_buscado)
                    df.columns = ['Fecha','Folio','Nombre','Producto','Cantidad','Precio']
                    df.set_index('Folio',inplace=True)
                    print("\n",df)
                    print(f"El total a pagar del Cliente {folio_nombre[0]} del Folio #{folio_buscar} es de ${folio_precio}")
                else:
                    print(f"No se encontró ningun registro con la clave {folio_buscar}")
            elif opcion_elegida == 3:
                fecha_consultar = input("Dime una fecha (dd/mm/aaaa): ")
                fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%d/%m/%Y").date()
                fecha_criterio = {"Fecha":fecha_consultar}
                c.execute("SELECT Fecha,Folio,Producto,Cantidad,Precio FROM DetalleVenta WHERE DATE(Fecha) = :Fecha;",fecha_criterio)
                fechas = c.fetchall()
                c.execute("SELECT SUM(PRECIO) FROM DetalleVenta WHERE DATE (Fecha) = :Fecha;",fecha_criterio)
                precio_fecha = c.fetchall()[0][0]
                precio_fecha = str(round(precio_fecha, 2))
                if fechas:
                    df=pd.DataFrame(fechas)
                    df.columns = ['Fecha','Folio','Producto','Cantidad','Precio']
                    df.set_index('Fecha',inplace=True)
                    print("\n",df)
                    print(f"Las ventas registradas en la Fecha {fecha_consultar} es de ${precio_fecha}")
                else:
                    print(f"No se encontró ningun registro con la fecha {fecha_consultar}")

except sqlite3.Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if (conn):
        conn.close()
        print("Se ha cerrado la conexión")              
                
                
    
         
         