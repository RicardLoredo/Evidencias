import pandas as pd
registro_ventas={"Producto":[],"Cantidad Ventas":[],"Precio":[],"Cliente":[]}
while (True):
    respuesta = 1
    respuesta_nombre=0
    print("MENU PRINCIPAL")
    print(" ")
    print("[1] Registrar Venta")
    print("[2] Consultar Venta")
    print("[X] Salir.")
    opcion_elegida = input("¿Qué deseas hacer?  > ")
    if opcion_elegida=="X" or opcion_elegida=="x":
        print("GRACIAS POR UTILIZAR EL PROGRAMA")
        break
    elif opcion_elegida=="1":
        while respuesta == 1:
            #se cicla el nombre del cliente ingresado
            while respuesta_nombre ==0:
                nombre = input ("\nDame el nombre del cliente: ") 
                break
            descripcion_articulo = input("Dime la descripcion del articulo: ")
            cantidad_piezas = input("Dime la cantidad de piezas: ")
            precio_venta = input("Dame el precio de venta: ")
            registro_ventas["Producto"].append(descripcion_articulo)
            registro_ventas["Cantidad Ventas"].append(cantidad_piezas)
            registro_ventas["Precio"].append(precio_venta)
            registro_ventas["Cliente"].append(nombre)
            ventas_registro = pd.DataFrame(registro_ventas)
            #se indexa los valores dentro del key 'Clientes'
            indexar_cliente =ventas_registro.set_index('Cliente')
            respuesta_nombre=int(input("\n ¿Deseas continuar con el mismo cliente? \n(1-Si / 0-No): "))
            respuesta = int(input("\n ¿Deseas capturar otro registro? \n(1-Si / 0-No): "))
            if respuesta ==0:
                #busca el valor de la variable nombre previamente ingresada
                nombre_ingresado=indexar_cliente.loc[nombre]
                #saca los valores que tiene la key 'precio'
                suma_precio=nombre_ingresado["Precio"]
                #como son strings los hace valores int
                for i in range(0,len(suma_precio)):
                    suma_precio[i] = int(suma_precio[i])
                suma=sum(suma_precio)
                print(f"El total a pagar del cliente {nombre} es de ${suma}")
    elif opcion_elegida=="2":
        consulta_venta = input ("\nIngresa el nombre del cliente a consultar: ")
        if consulta_venta in indexar_cliente.index:
            nombre_ingresado=indexar_cliente.loc[consulta_venta]
            print(nombre_ingresado)
        else:
            print("Ese cliente no esta registrado")
