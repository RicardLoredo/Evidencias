import os
import datetime
import pandas as pd
pd.set_option('mode.chained_assignment', None)
registro_ventas={"Fecha":[],"Cliente":[],"Folio":[],"Producto":[],"Cantidad Ventas":[],"Precio":[]}
folio=0
while (True):
    respuesta = 1
    print("MENU PRINCIPAL")
    print(" ")
    print("[1] Registrar Venta")
    print("[2] Consultar Venta")
    print("[3] Reporte de Ventas")
    print("[4] Salir.")
    opcion_elegida = int(input("¿Qué deseas hacer?  > "))
    if opcion_elegida == 4:
        print("GRACIAS POR UTILIZAR EL PROGRAMA")
        break
    elif opcion_elegida == 1:
        nombre = input("\nDame el nombre del cliente: ")
        folio = folio+1
        while respuesta == 1:
            descripcion_articulo = input("Dime la descripcion del articulo: ")
            cantidad_piezas = input("Dime la cantidad de piezas: ")
            precio_venta = int(input("Dame el precio de venta: "))
            fecha_actual = datetime.date.today()
            registro_ventas["Producto"].append(descripcion_articulo)
            registro_ventas["Cantidad Ventas"].append(cantidad_piezas)
            registro_ventas["Precio"].append(precio_venta)
            registro_ventas["Cliente"].append(nombre)
            registro_ventas["Fecha"].append(fecha_actual)
            registro_ventas["Folio"].append(folio)
            ventas_registro = pd.DataFrame(registro_ventas)
            #se indexa los valores dentro del key 'Clientes'
            indexar_cliente =ventas_registro.set_index('Cliente')
            respuesta = int(input("\n ¿Deseas capturar otro registro? \n(1-Si / 0-No): "))
            if respuesta == 0:
                #busca el valor de la variable nombre previamente ingresada
                nombre_ingresado=indexar_cliente.loc[nombre]
                #imprime el data frame
                print(nombre_ingresado)
                suma_precio=sum(nombre_ingresado["Precio"])
                print(f"El total a pagar del cliente {nombre} es de ${suma_precio}")
    elif opcion_elegida == 2:
        consulta_venta = input ("\nIngresa el nombre del cliente a consultar: \n")
        if consulta_venta in indexar_cliente.index:
            nombre_ingresado=indexar_cliente.loc[consulta_venta]
            print(nombre_ingresado)
            suma_precio=sum(nombre_ingresado["Precio"])
            print(f"El total a pagar del cliente {consulta_venta} es de ${suma_precio}")
        else:
            print("Ese cliente no esta registrado")
    elif opcion_elegida == 3:
        indexar_fecha =ventas_registro.set_index('Fecha')
        fecha_reporte = input("Dime la fecha para el reporte de ventas (dd/mm/aaaa):  \n")
        fecha_procesada = datetime.datetime.strptime(fecha_reporte, "%d/%m/%Y").date()
        if fecha_procesada in indexar_fecha.index:
            fecha = indexar_fecha.loc[fecha_procesada]
            print(fecha)
            suma_precio=sum(fecha["Precio"])
            print(f"El total de las ventas del dia {fecha_procesada} es de ${suma_precio}")
        else:
            print("No se encuentran reporte de ventas en esa fecha")
 
if os.path.isfile('registro_ventas.csv'):
    ventas_registro.to_csv(r'registro_ventas.csv',index=None,header=None,mode='a')
else:
    ventas_registro.to_csv(r'registro_ventas.csv',index=None,header=True)