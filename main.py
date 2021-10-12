#importamos las bibliotecas necesarias paa el funcionamiento del programa
import os #para el uso de os.system()
import csv #para el uso de csv.reader()
import datetime #para el uso de datetime.datetime.now()
import prettytable #para el uso de prettytable
from colorama import init, Fore, Back, Style


#inicializamos las variables globales
lista_datos=[] #lista que contendra los datos del archivo csv
archivo_csv='datos.csv' #nombre del archivo csv
init(autoreset=True)#inicializamos la biblioteca colorama   


################################################# Funciones-Interaccion con archivos #######################################################
#creamos una funcion que regrese True si el archivo csv existe, de lo contrario regresa False
def existe_archivo(archivo_csv):
    """ Verifica que el archivo exista dentro del directorio actual o de la ruta fijada"""
    if os.path.isfile(archivo_csv):
        return True
    else:
        return False
#funcion que lee el archivo csv, usamos DictionaryReader para leer el archivo y guardarlo en la lista_datos
def leer_archivo(archivo_csv):
    """Lee el archivo y va guardando cada registro en un diccionario con sus claves correspondientes, despues lo agrega a una lista y al final regresa la lista con los registros"""
    #verificamos si el archivo existe, con la funcion existe_archivo()
    if existe_archivo(archivo_csv):
        try:
            with open(archivo_csv,'r',encoding="utf8") as archivo:
                #un proceso importante es que utilizaremos la funcion dictreader() para leer el archivo csv
                registros=csv.DictReader(archivo)
                #recorremos el archivo csv y lo almacenamos en la lista lista_datos
                for registro in registros:
                    lista_datos.append(registro)
                #retornamos la lista lista_datos
                return lista_datos
        except FileNotFoundError:
            print('No se pudo abrir el archivo')
    else:
        print('El archivo no existe')





############################################################## Funciones-Interaccion con usuario #########################################################
#creamos nuestra primera funcion que es ver y contabilizar las rutas de importacion y exportacion
def importacion_exportacion(tipo):
    """Funcion que recibe un parametro tipo, que puede ser 'importacion' o 'exportacion' para saber que tipo de rutas se desea contabilizar"""
    #almacenamos en una variable el tipo de registros que se desea contabilizar (importacion o exportacion)
    tipo_registro=tipo
    #definimos una variable que almacene la cantidad de repeticiones de una ruta
    cantidad_repeticiones=0
    #creamos una lista que almacenara las rutas temporalmente ya sea de importacion o exportacion
    lista_rutas=[]
    #creamos una lisa que almacenara las rutas ya sea de importacion o exportacion y su cantidad de repeticiones
    lista_rutas_cantidad=[]
    #recorremos la lista lista_datos y vamos almacenando las rutas de importacion o exportacion en la lista lista_rutas
    for registro in lista_datos:
        #verificamos si trataremos con importacion o exportacion con un if 
        if registro['direction']==tipo_registro:
            #definismo una variable que almacenara la ruta 
            ruta = [registro["origin"], registro["destination"]]
            if ruta not in lista_rutas: #verificamos que la ruta no exista en la lista lista_rutas
                #ahora con un for vamos a contar la cantidad de repeticiones de la ruta
                for ruta_procesada in lista_datos:
                    if ruta == [ruta_procesada["origin"], ruta_procesada["destination"]]:
                        #aumentamos la cantidad de repeticiones de la ruta
                        cantidad_repeticiones += 1
                #registramos la ruta en la lista de rutas
                lista_rutas.append(ruta)
                #agregamos la ruta y su cantidad de repeticiones a la lista lista_rutas_cantidad
                lista_rutas_cantidad.append([ruta, cantidad_repeticiones])
                #reiniciamos la cantidad de repeticiones
                cantidad_repeticiones=0
    #orderamos la lista lista_rutas_cantidad de mayor a menor cantidad de repeticiones
    lista_rutas_cantidad.sort(key=lambda x: x[1],reverse=True)
    #retornamos el diccionario diccionario_rutas
    return lista_rutas_cantidad

def procesar_lista(lista_rutas_cantidad,opcion):
    """Funcion que recibe una lista de rutas y cantidad de repeticiones y calcula el porcentaje de cada ruta"""
    #creamos una lista que almacenara los porcentajes de cada ruta
    lista_procesada=[]
    if opcion == 1:
        #creamos una variable que almacenara la cantidad total de repeticiones
        cantidad_total=format(sum(lista_rutas_cantidad[i][1] for i in range(len(lista_rutas_cantidad))))
        #recorremos la lista lista_rutas_cantidad
        for ruta in lista_rutas_cantidad:
            #calculamos el porcentaje de cada ruta con base en la cantidad total de repeticiones
            porcentaje=round((ruta[1]/int(cantidad_total))*100,2)
            #agregamos la ruta y su porcentaje a la lista lista_procesada
            lista_procesada.append([ruta[0],ruta[1],porcentaje])
        #retornamos la lista lista_procesada
        return lista_procesada
    elif opcion == 2:
        #imprimimos l
        #creamos una variable que almacenara la cantidad total de valores
        cantidad_total=format(sum(lista_rutas_cantidad[i][2] for i in range(len(lista_rutas_cantidad))))
        for pais in lista_rutas_cantidad:
            #calculamos el porcentaje de cada ruta con base en la cantidad total de valores
            porcentaje=round((pais[2]/int(cantidad_total))*100,2)
            #agregamos la ruta y su porcentaje a la lista lista_procesada
            lista_procesada.append([pais[0],pais[1],pais[2],pais[3],porcentaje])
        #retornamos la lista lista_procesada
        return lista_procesada
    elif opcion == 3:
        #creamos una variable que almacenara la cantidad total de repeticiones
        cantidad_total=format(sum(lista_rutas_cantidad[i][2] for i in range(len(lista_rutas_cantidad))))
        #recorremos la lista lista_rutas_cantidad
        for tipo in lista_rutas_cantidad:
            #calculamos el porcentaje de cada ruta con base en la cantidad total de repeticiones
            porcentaje=round((tipo[2]/int(cantidad_total))*100,2)
            #agregamos la ruta y su porcentaje a la lista lista_procesada
            lista_procesada.append([tipo[0],tipo[1],tipo[2],porcentaje])
        #retornamos la lista lista_procesada
        return lista_procesada
    

def procesar_paises(tipo,lista_datos):
    """Funcion que procesa la lista de paises y cantidad de repeticiones y sumatoria de sus valores por cada exportacion/importacion"""
    #almacenamos en una variable el tipo de registros que se desea procesar (importacion o exportacion)
    tipo_registro=tipo
    pais_procesado = [] #lista que almacena los paises ya procesados
    value_pais = [] #

    #recorremos la lista lista_datos y contabilizamos suma de origen en base a tipo de registro
    for row in lista_datos:
        pais_actual = [tipo_registro, row["origin"]] #["Exports", "Mexico"] rescatamos el pais de origen
        valor = 0 #iniiciamos y cada ciclo de reiniciara la variable valor que almacenara la sumatoria de value de cada exportacion/importacion
        cantidad_de_operaciones = 0 #esta variable almacenara la cantidad de operaciones que realizo el pais de origen dependeiendo del tipo de registro
        
        if pais_actual in pais_procesado: #verificamos que el pais no haya sido procesado
            #si ya esta en la lista pais_procesado, entonces saltara al siguinete row(registro del for principal)
            continue #salta al siguiete registro
        #ahora con un loop vamos a contabilizar la sumatoria de value de cada exportacion/importacion
        for movimiento in lista_datos:
            if pais_actual == [movimiento["direction"], movimiento["origin"]]:
                valor += int(movimiento["total_value"]) #sumamos el value de cada registro que coeincida con el pais de origen
                cantidad_de_operaciones += 1 #incrementa la cantidad de operaciones que realizo el pais de origen
        pais_procesado.append(pais_actual) #agregamos el pais a la lista pais_procesado
        value_pais.append([tipo_registro, row["origin"], valor, cantidad_de_operaciones]) #agregamos el pais, el valor y la cantidad de operaciones a la lista value_pais
    value_pais.sort(reverse = True, key = lambda x:x[2])
    return value_pais

def procesar_transportes(tipo, lista):
    """Funcion que muestra los transportes mas utilizados en base a la cantidad de ventas"""
    lista_transportes = [] #lista que almacena los transportes mas utilizados
    lista_procesados = [] #lista que almacena los transportes ya procesados
    tipo_registro = tipo #almacenamos el tipo de registro que se desea procesar
    sumatoria_valores=0 #esta variable almacenara la sumatoria de valor de cada registro con relacion al tipo de registro y de transporte
    #recorremos la lista lista_datos y contabilizamos suma de origen en base a tipo de registro
    for row in lista:
        transporte_actual = [tipo_registro, row["transport_mode"]] #["Exports", "Truck"] rescatamos el transporte de origen
        cantidad_de_operaciones = 0 #esta variable almacenara la cantidad de operaciones que realizo el transporte de origen dependeiendo del tipo de registro
        if transporte_actual in lista_procesados: #verificamos que el transporte no haya sido procesado
            #si ya esta en la lista pais_procesado, entonces saltara al siguinete row(registro del for principal)
            continue #salta al siguiete registro
        #ahora con un loop vamos a contabilizar la sumatoria de value de cada exportacion/importacion
        for movimiento in lista:
            if transporte_actual == [movimiento["direction"], movimiento["transport_mode"]]:
                cantidad_de_operaciones += 1 #incrementa la cantidad de operaciones que realizo el pais de origen
                sumatoria_valores += int(movimiento["total_value"]) #sumamos el value de cada registro que coeincida con el pais de origen
        lista_procesados.append(transporte_actual) #agregamos el pais a la lista pais_procesado
        lista_transportes.append([row["transport_mode"], cantidad_de_operaciones,sumatoria_valores]) #agregamos el pais, el valor y la cantidad de operaciones a la lista value_pais
    lista_transportes.sort(reverse = True, key = lambda x:x[2])
    return lista_transportes
    



############################################################## UX/UI #########################################################
#creamos una funcion que nos permita crear un menú para el usuario
def menu():
    #Definimos un objeto de tipo datetime.datetime
    fecha_actual=datetime.datetime.now()
    #imprimimos un mensaje de bienvenida al usuario con el nomnbre del la empresa color amarillo
    print(Fore.GREEN+'Bienvenido al sistema de registro de datos de '+Fore.YELLOW+'Synergy Logistics       Fecha:',fecha_actual.strftime('%d/%m/%Y %H:%M:%S'))
    #definismos un objeto de tipo prettytable
    menu=prettytable.PrettyTable()
    #agregamos las columnas al objeto menu
    menu.field_names=['Opciones','Descripcion']
    #agregamos los datos al objeto menu
    menu.add_row(['1','Conclusiones y recomendaciones'])
    menu.add_row(['2','Top 10 de las rutas de importación con mayor demanda'])
    menu.add_row(['3','Top 10 de las rutas de exportación con mayor demanda'])
    menu.add_row(['4','Top 3 de los medios de transporte de mayor importancia'])
    menu.add_row(['5','Valor total de importaciones - paises'])
    menu.add_row(['6','Valor total de exportacione - paises'])
    menu.add_row(['7','Salir'])
    #imprimimos el menu color azul con fondo blanco
    print(Fore.BLUE+Style.BRIGHT+str(menu))

def imprimir_tabla(opcion,lista):
    """Es funcion nos ayudara a imprimir las tablas de todo el programa"""
    #creamos un objeto de tipo prettytable
    tabla=prettytable.PrettyTable()
    #creamos una variable que almacenara la sumatoria de las repeticiones de las rutas
    total=round((sum(lista[i][2] for i in range(len(lista)))), 2)
    #variable que almacenara el porcentaje de cada ruta en base a la cantidad de datos analizados
    subtotal=0
    #agregamos las columnas al objeto tabla
    if opcion==1:
        tabla.field_names=[Fore.YELLOW+'Ruta'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Cantidad - Importaciones'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Porcentaje'+Fore.LIGHTWHITE_EX]
    elif opcion==2:
        #creamos una variable que almacenara la sumatoria de las repeticiones de las rutas
        total=round((sum(lista[i][2] for i in range(len(lista)))), 2)
        cal_subtotal=2
        valor=10
        tabla.field_names=[Fore.YELLOW+'Ruta'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Cantidad - Importaciones'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Porcentaje'+Fore.LIGHTWHITE_EX]
    elif opcion==3:
        #creamos una variable que almacenara la sumatoria de las repeticiones de las rutas
        total=round((sum(lista[i][2] for i in range(len(lista)))), 2)
        cal_subtotal=2
        valor=10
        tabla.field_names=[Fore.YELLOW+'Ruta'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Cantidad - Exportaciones'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Porcentaje'+Fore.LIGHTWHITE_EX]
    elif opcion==4:
        #creamos una variable que almacenara la sumatoria de las repeticiones de las rutas
        total=round((sum(lista[i][3] for i in range(len(lista)))), 2)
        cal_subtotal=3
        valor=len(lista)
        tabla.field_names=['Medio de transporte','Cantidad - Importaciones', 'Ventas - valor','Porcentaje']
    elif opcion==5:
        total=round((sum(lista[i][3] for i in range(len(lista)))), 2)
        cal_subtotal=3
        valor=len(lista)
        tabla.field_names=['Medio de transporte','Cantidad - Exportaciones','Ventas - valor','Porcentaje']

    for i in range(valor):
        subtotal+=lista[i][cal_subtotal]
        #agregamos los datos al objeto tabla_exportaciones, la variable i nos ayudara a identificar cual es la ruta
        #imrpimimos el total de repetienciones en formato de con comas
        if valor==10:
            tabla.add_row([lista[i][0][0]+' - '+lista[i][0][1],format(lista[i][1],',.0f'),format(lista[i][2])+'%'])
        if valor != 10:
            tabla.add_row([lista[i][0],format(lista[i][1],',.0f'),format(lista[i][2],',.0f'),format(lista[i][3])+'%'])
    #imprime total de la tabla
    print(Fore.GREEN+'Estos datos representan el '+Fore.YELLOW+str(round(subtotal,2))+'%'+Fore.GREEN+' del porcentaje total que es: '+Fore.YELLOW+str(total)+'%')
    #regresa el objeto tabla
    return tabla

def imprimir_tabla_paises(opcion,lista):
    """Es funcion nos ayudara a imprimir las tablas de la parte donde se solicita el 80 %"""
    #creamos un objeto de tipo prettytable
    tabla=prettytable.PrettyTable()
    #declaramos una variable que almacenara el total de porcentaje de datos que se analizaron
    subtotal=0.0
    #total alamcena la sumatria de todos los procejntos de los paises de la lista}
    total=round((sum(lista[i][4] for i in range(len(lista)))), 2)
    if opcion==1:
        #agregamos las columnas al objeto tabla
        tabla.field_names=[Fore.YELLOW+'Tipo'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'País'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Valor - Exportaciones'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Cantidad de operaciones'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Porcentaje'+Fore.LIGHTWHITE_EX]   
    elif opcion==2:
        #agregamos las columnas al objeto tabla
        tabla.field_names=[Fore.YELLOW+'Tipo'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'País'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Valor - Importaciones'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Cantidad de operaciones'+Fore.LIGHTWHITE_EX,Fore.YELLOW+'Porcentaje'+Fore.LIGHTWHITE_EX]
    #antes de pasar la lista a imprimir en este caso le haremos un procesamiento para
    ochenta_porciento_lista=[] #creamos una lista temporal que almacenara los datos que den la suma del 80%
    valor_pais=0 
    porcentaje=80 #definimos el 80%
    #recorremos la lista y extraemos el apartado de valores
    for pais in lista:
        #ahora lo que haremos es crear una variable que vaya acumulado los valores de cada pais
        valor_pais += (pais[4])
        #verificamos que la suma que esta en al variable valor_pais sea menor o igual a 80.0
        if valor_pais <= 80.0:
            #si es menor o igual a 80.0 entonces agregamos el pais a la lista temporal
            ochenta_porciento_lista.append([pais[0],pais[1],pais[2],pais[3],pais[4]])
        else:
            #si es mayor a 80.0 entonces terminamos el ciclo
            break
    #ahora que ya tenemos la lista temporal con los paises que sumando sus porcentajes nos dan el 80% o menos recorremos la lista temporal
    for lista in ochenta_porciento_lista:
        subtotal+=lista[4]
        tabla.add_row([lista[0],lista[1],format(lista[2],',.0f'),format(lista[3],',.0f'),format(lista[4],',.2f')+'%'])
    print(Fore.GREEN+'Estos datos representan el '+Fore.YELLOW+str(round(subtotal,2))+'%'+Fore.GREEN+' del porcentaje total que es: '+Fore.YELLOW+str(total)+'%')
    #regresa el objeto tabla
    return tabla

def conclusiones(lista_datos):
    """Esta funcion tiene el objetivo en particular de llamar a todas las funciones"""
    #crearemos una lista con las inetrrogantes a responder gracias a los resultados realizados en el programa
    lista_interrograntes=[
        " Acorde a los flujos de importación y exportación, ¿cuáles son esas 10 rutas? ¿le conviene implementar esa estrategia? ¿porqué?",
        "¿Cuáles son los 3 medios de transporte más  importantes  para  Synergy  logistics  considerando  el  valor  de  las importaciones  y  exportaciones?  ¿Cuál  es  medio  de  transporte  que    podrían reducir?",
        "Si Synergy Logistics quisiera  enfocarse  en  los  países  que  le  generan  el  80%  del  valor  de  las exportaciones e importaciones  ¿en qué grupo de países debería enfocar sus esfuerzos?"
    ] 
    print(Fore.RED+'Próposito: '+Fore.LIGHTWHITE_EX+'A partir de los datos generar un análisis que sirva de la base para la estructuración de su estrategia operativa.')
    #coemnzamos a contestar las preguntas, recorremos la lista de preguntas y empezamos a contestar con las funciones
    #pregunta uno
    print(Fore.RED+'Pregunta 1:'+Fore.LIGHTWHITE_EX+lista_interrograntes[0])
    print(Fore.LIGHTWHITE_EX+str((imprimir_tabla(2,procesar_lista(importacion_exportacion("Imports"),1)))))
    print(Fore.LIGHTWHITE_EX+Style.BRIGHT+str((imprimir_tabla(3,procesar_lista(importacion_exportacion("Exports"),1)))))
    respuesta_uno="""Considerando la tabla de arriba, Synergy Logistics tiene rutas de importación y exportación que son complementarias entre sí, es decir, que se exportan y se importan de un misma ruta lo que denota que el comercio se encuentra activo en ambos países, ádemas que las primeras 10 rutas de importación representan el 47.41% de todas sus importaciones y las primera 10 rutas de exportación representan solamente el 21.45% por lo que en este caso Synergy Logistics, debería enfocarse en mejorar sus rutas de exportacion y mantener las rutas de importación.
    """
    print(Fore.GREEN+'Respuesta: '+Fore.LIGHTWHITE_EX+respuesta_uno)

    #pregunta dos
    print(Fore.RED+'Pregunta 2:'+Fore.LIGHTWHITE_EX+lista_interrograntes[1])
    #llamamos a la funcion procesar_transportes
    print(Fore.LIGHTWHITE_EX+str(imprimir_tabla(4,procesar_lista(procesar_transportes("Imports",lista_datos),3))))
    #llamamos a la funcion procesar_transportes
    print(Fore.LIGHTWHITE_EX+str(imprimir_tabla(5,procesar_lista(procesar_transportes("Exports",lista_datos),3))))
    respuesta_dos=""" En base a los resultados y las ventas por asi decirlo que genero cada medio, Synergy Logistics debería enfocarse en reducir los medios de trasnporte de MAR, ya que en cantidad son mayores tanto en las exportaciones como en las importaciones pero este medio genera ventas menores. a lo que normalmente se hace en otros medios por ello cosnidero que el enfoque debe ser en reducir los envios(maritimos)
    """
    print(Fore.GREEN+'Respuesta: '+Fore.LIGHTWHITE_EX+respuesta_dos)

    #pregunta tres
    print(Fore.RED+'Pregunta 3:'+Fore.LIGHTWHITE_EX+lista_interrograntes[2])
    print(Fore.LIGHTWHITE_EX+str((imprimir_tabla_paises(2,procesar_lista(procesar_paises("Imports",lista_datos),2)))))
    print(Fore.LIGHTWHITE_EX+str((imprimir_tabla_paises(1,procesar_lista(procesar_paises("Exports",lista_datos),2)))))

    respuesta_tres=""" Como se muestra en la tabla de arriba el enfoque que le deben dar la empresa Synergy Logistics es los paises como China, Japon, Francia, EUA, Alemania entre otros, ya que estos representan la mayor parte de sus ingresos por ello lo mejor es mantener y esforzarce más en los paises que se muestran arriba  """
    print(Fore.GREEN+'Respuesta: '+Fore.LIGHTWHITE_EX+respuesta_tres)
        

#funcion main
def main():
    #llamamos a la funcion leer_archivo()
    leer_archivo(archivo_csv)
    #definimos una variable opcion
    opcion=0
    #definimos una variable salir
    salir=False
    #definimos una variable para el ciclo while
    while salir==False:
        #llamamos a la funcion menu()
        menu()
        #pedimos al usuario que ingrese una opcion y validamos que sea un numero entero
        opcion=input('Ingrese una opcion: ')
        #validamos que la opcion sea un numero entero con isdigit()
        if opcion.isdigit():
            #convierte la variable opcion a entero con int()
            opcion=int(opcion)
            #validamos que la opcion sea un numero entero entre 1 y 7
            if opcion>=1 and opcion<=7:
                #validamos que la opcion sea 1
                if opcion==1:
                    #llamamos a la funcion conclusiones()
                    conclusiones(lista_datos)
                #validamos que la opcion sea 2
                elif opcion==2:
                    #llamamos a la funcion procesar_lista()
                    lista_importaciones=procesar_lista(importacion_exportacion("Imports"),1)
                    print(Fore.RED+'Top 10 de las rutas de importaciones con mayor demanda')
                    #mandamos llamar a la funcion imprimir_tabla() y le mandamos la opcion 1 y la lista_exportaciones
                    tabla_importaciones=(imprimir_tabla(2,lista_importaciones))
                    #imprimimos la tabla color verde 
                    print(Fore.LIGHTWHITE_EX+str(tabla_importaciones))
                elif opcion==3:
                    #llamamos a la funcion procesar_lista()
                    lista_exportaciones=procesar_lista(importacion_exportacion("Exports"),1)
                    print(Fore.RED+'Top 10 de las rutas de exportación con mayor demanda')
                    #mandamos llamar a la funcion imprimir_tabla() con los parametros opcion=2 y lista=lista_exportaciones
                    tabla_exportaciones=(imprimir_tabla(3,lista_exportaciones))
                    print(Fore.LIGHTWHITE_EX+Style.BRIGHT+str(tabla_exportaciones))
                #validamos que la opcion sea 4
                elif opcion==4:
                    print(Fore.RED+'Top de medios de transpporte en base a sus exportaciones e importaciones')
                    #llamamos a la funcion procesar_transportes
                    lista_trans_importa=procesar_transportes("Imports",lista_datos)
                    lista_procesada_impor=procesar_lista(lista_trans_importa,3)
                    tabla_impor=imprimir_tabla(4,lista_procesada_impor)
                    print(Fore.RED+"Importaciones: ")
                    print(Fore.LIGHTWHITE_EX+str(tabla_impor))
                    #llamamos a la funcion procesar_transportes
                    lista_trans_export=procesar_transportes("Exports",lista_datos)
                    lista_procesada_export=procesar_lista(lista_trans_export,3)
                    tabla_export=imprimir_tabla(5,lista_procesada_export)
                    print(Fore.RED+"Exportaciones: ")
                    print(Fore.LIGHTWHITE_EX+str(tabla_export))
                #validamos que la opcion sea 5
                elif opcion==5:
                    valores_paises =procesar_paises("Imports",lista_datos)
                    lista_valor_paises=procesar_lista(valores_paises,2)
                    print(Fore.RED+'Top de paises que aportanel 80% de las importaciones')
                    #mandamos llamar a la funcion imprimir_tabla_paises() con los parametros opcion=2 y lista=lista_valor_paises    
                    tabla_paises=(imprimir_tabla_paises(2,lista_valor_paises))
                    print(Fore.LIGHTWHITE_EX+str(tabla_paises))
                #validamos que la opcion sea 6
                elif opcion==6:
                    valores_paises = procesar_paises("Exports",lista_datos)
                    lista_valor_paises=procesar_lista(valores_paises,2)
                    print(Fore.RED+'Top de paises que aportanel 80% de las exportaciones')
                    #mandamos llamar a la funcion imprimir_tabla_paises() con los parametros opcion=1 y lista=lista_valor_paises
                    tabla_paises=(imprimir_tabla_paises(1,lista_valor_paises))
                    print(Fore.LIGHTWHITE_EX+str(tabla_paises))
                #validamos que la opcion sea 7
                elif opcion==7:
                    #cambiamos el valor de la variable salir
                    salir=True
            else:
                #mostramos un mensaje de error en caso de que la opcion no sea un numero entre 1 y 7 color rojo
                print(Fore.RED+'Opcion no valida '+ Fore.YELLOW+ "Ingresea una opcion entre 1 y 7")
        else:
            #imprimimos un mensaje de error color rojo 
            print(Fore.RED+'Ingresa un número '+Fore.YELLOW+'entero')

#si la funcion main() existen ejeucta la funcion main()
if __name__=='__main__':
    main()


