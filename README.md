# MCOC2021-P3-Grupo09

Integrantes:
 * Enzo Bertinelli
 * Daniel Morales
 * Tomas Vergara

# ENTREGA 2

Los costos asociados a las rutas están medidos en minutos.

![image](https://user-images.githubusercontent.com/89056734/141026125-53b7139b-e4cc-41a4-9216-8c195f8ce38c.png)

![image](https://user-images.githubusercontent.com/89056734/141026157-27786e96-f662-4ab5-8f91-dd787c19f3b6.png)

![image](https://user-images.githubusercontent.com/89056734/141026183-e2cde269-e4d5-4b2b-869c-926bcdad0a0a.png)

![image](https://user-images.githubusercontent.com/89056734/141026200-cec7b2d7-0b04-405f-89a0-20a4053f6c94.png)


# ENTREGA 3 - Daniel Morales

![Figure_1](https://user-images.githubusercontent.com/88337429/141601874-8e994426-7bee-4810-b04b-a1623108185b.png)

![Figure_2](https://user-images.githubusercontent.com/88337429/141601875-a4e5673b-29b4-4870-9b8d-9c540eb1cea9.png)

Se presenta la imagen generada de la zona donde vivo, ortuzar 140. Junto con la zona del enunciado como ejemplo del funcionamiento del codigo.

# ENTREGA 4


![arcosp3e4](https://user-images.githubusercontent.com/88337429/141875711-918ec6a1-6708-4b6c-a202-55ec527c6583.png)
![arcos2p3e4](https://user-images.githubusercontent.com/88337429/141875716-8c814ab5-2be0-457a-8bd0-05ba0362e9d6.png)
![funcion_costo](https://user-images.githubusercontent.com/88337429/142093858-dc798c6b-2409-464e-9a14-2f7244029199.png)


![wardrop1](https://user-images.githubusercontent.com/88337429/141875719-81707188-acb1-4c72-99e4-c5071fafc50d.PNG)
![wardrop2](https://user-images.githubusercontent.com/88337429/141875725-a49be0f6-f945-4b81-8175-aba9ff43af23.PNG)

Algoritmo utilizado:
```Python
while True:
    se_asigno_demanda=False
    for key in OD:
        demanda_actual = OD[key]
        demanda_objetivo=OD_target[key]

        if demanda_actual>0:
            
            path=dijkstra_path(G,key[0],key[1], weight=costo)
            #incrementar flujo en ruta minima
            Nparadas =len(path)
            
            for i_parada in range(Nparadas-1):
                o=path[i_parada]
                d= path[i_parada+1]
                flujo_antes=G.edges[o,d]["flujo"]
                #G.edges[o,d]["flujo"]+=0.1
            #OD[key]-=0.1
                G.edges[o,d]["flujo"]+=OD_target[key]/1000
            OD[key]-=OD_target[key]/1000
            se_asigno_demanda=True
    if not se_asigno_demanda: break
```     
Tras la creacion del diccionario con los valores de la matriz OD se crea una copia llamada OD_target, ambos diccionarios son utilizados para iterar de acuerdo a cuantos viajes faltan por realizar para cumplir con la matriz OD.

Estas iteraciones son posibles gracias al uso de dijkstra_path para encontrar la ruta mas barata para enviar el viaje de cada iteracion de acuerdo a los costos de la iteracion anterior hasta que se hayan iterado todos los pares OD y la demanda sea satisfecha.

En cada iteracion se decidio enviar una cantidad de viajes proporcionales a la demanda del par OD para lograr obtener una mejor convergencia.

Se puede ver que esta entrega se hace el equilibrio si hizo a travez de los arcos, y no de las rutas. Esto se hace ya que con las rutas quedan mas incognitas que ecuaciones, por ende, habrían infinitas soluciones.

Con respecto a las rutas utilizadas, según wardrop, solo se utilizaran las rutas que tengan costos iguales o/y minimos, de esta forma, quedaran rutas sin utilizar, hasta que las otras rutas, que se estaban utlizando, se conjestionen o aumenten su costo. 

Como modo de contexto, wardrop afirma que una vez llegado al equilibiro, como es el caso de esta tarea, ningun usuario, puede reducir unilateralmente su costo mediante el cambio de ruta. 
De esta forma, las rutas utilizadas para los distintos pares origen destino serán solo las destacadas en el excel.

A continuación se presentan los errores porcentuales al sacar los costos y flujos de los  pares orígenes - destino. Tal como puede apreciarse, ninguno de ellos superó el 1%, lo cual es un muy buen indicador de la exactitud del código implementado.

![image](https://user-images.githubusercontent.com/89056734/142055571-8ea08c41-288c-43b9-bbc4-42ea28d4d781.png)


ENTREGA 5

Para seleccionar y posteriormente delimitar las zonas a incluir, seinvestigó por donde efectivamente pasa AVO. Luego, en la página "red CADEUS" se ubicaron las zonas por donde este nuevo proyecto pasaba y se delimitaron mediante "edges" en el programa. Se muestra n la figura como las zonas seleccionadas fueron las que están por la perfiferia del actual Américo Vespucio, es decir, las zonas 146, 666, 683, 682, 677, 287, 307, 288, 291, etc.

Quedaron seleccionadas aproximadamente 14 zonas en el mapa, y algunos fragmentos de otras.

![image](https://user-images.githubusercontent.com/89056734/142709200-515be144-6a71-41e5-9e98-3ac270fc0e44.png)

Debido a la lejanía y la expedita conexión una vez construida AVO, las zonas 146 y 289 en adelante (en el mapa) serán los pares OD con mayor flujo y/o demanda al momento en que la gigantesca obra vial esté terminada.

