import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import dijkstra_path

f1= lambda f: 10+f/120
f2= lambda f: 14+f/80
f3= lambda f: 10+f/240

#matriz origen destino
OD= {
     ("A","C"):1100,
     ("A","D"):1110,
     ("A","E"):1020,
     ("B","C"):1140,
     ("B","D"):1160,
     ("C","E"):1170,
     ("C","G"):1180,
     ("D","C"):350,
     ("D","E"):1190,
     ("D","G"):1200,
     }

#una copia

OD_target=OD.copy()

G=nx.DiGraph()

G.add_node("A", pos=(1,5))
G.add_node("B", pos=(1,3))
G.add_node("C", pos=(3,3))
G.add_node("D", pos=(3,1))
G.add_node("E", pos=(5,5))
G.add_node("G", pos=(5,3))

G.add_edge("A","B", fcosto=f1, flujo=0, costo=0,ffcosto="10+f/120")#r
G.add_edge("A","C", fcosto=f2, flujo=0, costo=0,ffcosto="14+f/80")#s

G.add_edge("B","C", fcosto=f3, flujo=0, costo=0,ffcosto="10+f/240")#t
G.add_edge("B","D", fcosto=f2, flujo=0, costo=0,ffcosto="14+f/80")#u

G.add_edge("D","C", fcosto=f1, flujo=0, costo=0,ffcosto="10+f/120")#v
G.add_edge("D","G", fcosto=f2, flujo=0, costo=0,ffcosto="14+f/80")#y

G.add_edge("C","G", fcosto=f3, flujo=0, costo=0,ffcosto="10+f/240")#x
G.add_edge("C","E", fcosto=f2, flujo=0, costo=0,ffcosto="14+f/80")#w

G.add_edge("G","E", fcosto=f1, flujo=0, costo=0,ffcosto="10+f/120")#z

def costo(ni,nf,attr):
    funcosto_arco=attr["fcosto"]
    flujo_arco=attr["flujo"]
    return funcosto_arco(flujo_arco)
#demanda=1000
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
                #print(OD_target[key]/1000)
            OD[key]-=OD_target[key]/1000
            se_asigno_demanda=True
    if not se_asigno_demanda: break
    
for ni,nf in G.edges:
    arco =G.edges[ni,nf]
    funcosto_arco=arco["fcosto"]
    flujo_arco=arco["flujo"]
    arco["costo"]=funcosto_arco(flujo_arco)
    
pos=nx.get_node_attributes(G,"pos")

plt.figure()

ax1=plt.subplot(1, 1, 1)

nx.draw_networkx_nodes(G, pos=pos)
nx.draw_networkx_labels(G, pos=pos)
nx.draw_networkx_edges(G, pos=pos,width=1.5)
labels=nx.get_edge_attributes(G,"ffcosto")
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.suptitle(f"Funcion costo")
plt.grid(True)
plt.show()
    
plt.figure()

ax1=plt.subplot(1, 1, 1)

nx.draw_networkx_nodes(G, pos=pos)
nx.draw_networkx_labels(G, pos=pos)
nx.draw_networkx_edges(G, pos=pos,width=1.5)
labels=nx.get_edge_attributes(G,"flujo")
for i in labels:
    #print(labels[i])
    labels[i]=format(labels[i], '.4f')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.suptitle(f"Flujos arcos")
plt.grid(True)
plt.show()

plt.figure()
ax1=plt.subplot(1, 1, 1)

#nx.draw(G,pos,with_labels=True, font_weight="bold")
nx.draw_networkx_nodes(G, pos=pos)
nx.draw_networkx_labels(G, pos=pos)
nx.draw_networkx_edges(G, pos=pos,width=1.5)
labels=nx.get_edge_attributes(G,"costo")
for i in labels:
    #print(labels[i])
    labels[i]=format(labels[i], '.4f')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
#plt.suptitle(f"Andate por {path}")
plt.suptitle(f"Costos arcos")
plt.grid(True)
plt.show()
###
#plt.figure()
#ax = plt.subplot(1, 1, 1)
#nx.draw_networkx_nodes(G, pos=pos)
#nx.draw_networkx_labels(G, pos=pos)
#nx.draw_networkx_edges(G, pos=pos)
#nx.draw_networkx_edges(G, pos, edgelist=edgelist, edge_color=colores)
#nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
#x=[0,1,2,3,4,5,6,7,8,9,10]
#xlabels=["0","1","2","3","4","5","6","7","8","9","10"]
#y=[0,1,2,3,4,5,6,7,8,9,10]
#ylabels=["0","1","2","3","4","5","6","7","8","9","10"]
#plt.xticks(x, xlabels)
#plt.yticks(y, ylabels)
#ax.xaxis.set_ticks_position('bottom')
#ax.yaxis.set_ticks_position('left')
#plt.grid(True)

#plt.xlabel("X (km)")
#plt.ylabel("Y (km)")


#plt.show()


#print(labels)
#for i in labels:
#    print(labels[i])
#    labels[i]=format(labels[i], '.2f')
#print(labels)

#xx=(nx.all_simple_paths(G,"A","B"))
#for i in xx: print(i)
print("\n")
print("Revisar cumplimiento de wardrop")
for key in OD:
    print(f"Par OD: {key}")
    #print("\n")
    c=nx.all_simple_paths(G,key[0],key[1])
    for path in c:
        Nparadas =len(path)
        #print(path)
        #print(Nparadas)
        Costo_ruta=0
        for i_parada in range(Nparadas-1):
            o=path[i_parada]
            d= path[i_parada+1]
            Costo_ruta+=G.edges[o,d]["costo"]
        Costo_ruta=format(Costo_ruta, '.4f')
        print(f"Ruta: {path} Costo:{Costo_ruta}")
    print("\n")








