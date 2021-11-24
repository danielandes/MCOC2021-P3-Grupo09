import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gps
import pandas
import numpy as np
from networkx.algorithms import dijkstra_path
zonas_gdf = gps.read_file("eod.json")
ox.config(use_cache=True, log_console=True)
#zonass=[18,12,17,19,13,20,49,50,48]
zonass=[146,590,683,682,666,684,677,306,287,307,288,291,289,290,304,266,434,269,267,281,435,147,148,145,153,598,597,599,
        587,678,667,669,508,507,496,505,512,504,305,291,307,320,306,668,292,433,432,509,282,283,284,426.579,144,578,143,
        88,89,87,92,95,94,93,151,579,426,440,278,280,279,439,438,442,436,471,666,683,682,677,287,307,306,288,291,289,290,
        304,266,434,267,435,281,426,283,440,278,439,471,422,470,371,469,370,476,368,487,367,467,360,367,482,198,206,197,
        225,227,213,231,214,246,243,242,240,241,665,661,
        443,444,441,364,369,488,474,473,472,473,474,488,489,477,485,475,486,483,468,373,372,377,375,196,224,223,199,200,234,245,246,243,242,
        226,660,663,662,664,657,656,659.658,654,236,249,237,238,239,235,239,238,237,249,623,649,
        625,638,637,624,623,649,647,376,636,630,633,634,646,645,631,632,635,374,
        361,621,620,629,622,628,641,244,374,362,363,365,366,627,626,619,639,640,365,366,29,
        30,38,52,427,420,428,423,428,420,421,51,52,37,36,31,45,46,44,43,42,35,447,448,424,437,425,429,
        431,430,419,446,514,502,501,495,32,33,34,47,48,50,49,16,513,510,511,494,41,23,516,498,506,591,586,595,596,594,
        503,21,22,19,17,12,13,18,20,11,10,9,8,165,593,164,167,592,593,585,589,584,
        581,582,160,162,161,163,170,171,159,168,158,86,85,96,90,98,
        445,601,600,515,499,497,500,169,157,166,583,588,580,99,84,97
        ]#,24,455,457,458
zonas_seleccionadas=zonas_gdf[zonas_gdf["ID"].isin(zonass)] #Centro + bordes
north=-33.3637
west=-70.80
south=-33.56
east=-70.5240
#north=-33.34
#west=-70.645
#south=-33.445
#east=-70.555
#north=-33.425
#west=-70.665
#south=-33.455
#east=-70.640
G=ox.graph_from_bbox(
    north=north,
    south=south,
    east=east,
    west=west,
    network_type="drive",
    #clean_periphery=True,
    #custom_filter='["highway"~"motorway|primary|construction"]',
    custom_filter='["highway"~"motorway|primary|construction|secondary|tertiary"]',
    #custom_filter='["highway"~"motorway|primary|secondary|tertiary"]',
    )

#a,b=ox.graph_to_gdfs(G)
#plt.figure()
#ax=plt.subplot(111)
#b.plot(ax=ax)
#plt.show()
datoseod=pandas.read_csv("mod.csv")
#print(datoseod)
indexes=datoseod.index
DiccionarioMatrizOD={}
for i in indexes:
    ni=int(datoseod.loc[i]["398"])
    nf=int(datoseod.loc[i]["398.1"])
    valor=datoseod.loc[i]["687.03176715"]
    if ni in zonass and nf in zonass and ni!=nf:
        DiccionarioMatrizOD[(ni,nf)]=valor
print(DiccionarioMatrizOD) 
print(len(DiccionarioMatrizOD)) 
contadorviajes=0
for key in DiccionarioMatrizOD:
    contadorviajes+=DiccionarioMatrizOD[key]
print(f"viajes totales = {contadorviajes}")
    #print(datoseod.loc[i]["398"],datoseod.loc[i]["398.1"],datoseod.loc[i]["687.03176715"])


gdf_nodes,gdf_edges = ox.graph_to_gdfs(G)
#print(gdf_nodes.loc[4441169826])
street_centroids=gdf_edges.centroid
#print(gdf_edges.iloc[0])
#386184
#224218562
#print(gdf_nodes.loc[386184])
#print(gdf_nodes.loc[224218562])
#exit()

plt.figure()
ax=plt.subplot(111)
#zonas_seleccionadas2=zonas_gdf[zonas_gdf["ID"].isin([146])] #Centro

centroides_seleccionados=zonas_seleccionadas.centroid

cont=0
gdf_nodes=gps.clip(gdf_nodes, zonas_seleccionadas)    
for idx,row in zonas_seleccionadas.iterrows(): 
    #print(row["ID"], idx)
    c=row.geometry.centroid
    ax.annotate(text=row["ID"], xy=(c.x,c.y), horizontalalignment="center")
zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")
#zonas_seleccionadas2.plot(ax=ax, color="#FFB2B2")
centroides_seleccionados.plot(ax=ax, marker="o", color="red", markersize=5)
nodoos=gps.clip(gdf_nodes, zonas_seleccionadas)

#print(nodoos.head())
#for head in nodoos.head(): print(head)

#print("")
#print(gdf_edges.iloc[2])
#print(gdf_edges.head())
#for head in gdf_edges.head(): print(head)
plt.show()

nodoos,gdf_edges = ox.graph_to_gdfs(G)

gdf_edges=gps.clip(gdf_edges, zonas_seleccionadas)
clipn=gps.clip(nodoos, zonas_seleccionadas)
clipn=clipn.index
#print(nodoos.index)
#print(nodoos.loc[386138])
listaidnodos=nodoos.index
#for i in listaidnodos: print(i)
#print(listaidnodos)
#print(gdf_edges.index[0])
#print("espaciador")
listaidedges=gdf_edges.index
#posibles=["motorway","secondary","tertiary","primary","residential"]
#posibles=["secondary","tertiary"]
#for i in listaidedges:
    #if gdf_edges.loc[i]["highway"] in posibles:
        
        #S.add_edge(i[0],i[1], fcosto=0, flujo=0, costo=0)
        #print("ayoo")
S=nx.Graph()
listanod=[]
#print(gdf_edges.iloc[10])
f1= lambda q, p, L, v, u: float(L)/float(v) + (float(u)-5)*12 + (900/(float(u)*float(p)))*(10*float(q) - float(u)*float(p) + np.sqrt((10*float(q)-float(u)*float(p))**2 + float(q)/9)) if float(L)/float(v) + (float(u)-5)*12 + (900/(float(u)*float(p)))*(10*float(q) - float(u)*float(p) + np.sqrt((10*float(q)-float(u)*float(p))**2 + float(q)/9)) > 0 else 0
#for i in clipn:
#    S.add_node(i, pos=[nodoos.loc[i]["x"],nodoos.loc[i]["y"]], index=i)
for i in listaidedges:
    if i[0] in clipn and i[1] in clipn:
        tipo=gdf_edges.loc[i]["highway"]
        nombre_e=gdf_edges.loc[i]["name"]
        L_atr=float(gdf_edges.loc[i]["length"])
        p_atr=gdf_edges.loc[i]["lanes"]
        if isinstance(p_atr, list):
            p_atr=float(max(p_atr))
    #
    #
        linew=1
        if tipo=="motorway": 
            color="orange"#
            u_atr=5
            v_atr=25
        elif tipo=="secondary": 
            color="green"#
            u_atr=3
            v_atr=15
        elif tipo=="tertiary": 
            color="blue"#
            u_atr=2
            v_atr=8
        elif tipo=="primary": 
            color="yellow"#
            u_atr=3
            v_atr=15
        #elif tipo=="residential": 
            #color="black"#
            #u_atr=2
            #v_atr=8
        elif tipo=="construction": 
            #print("aha",gdf_edges.loc[i]["highway"],gdf_edges.loc[i]["name"])
            #color="red" 
            #linew=1
            #u_atr=5
            #v_atr=25
            tipo=""
        #elif tipo=="residential": color="black"#black
        else: tipo=""
        if tipo!="":
            oneway=gdf_edges.loc[i]["oneway"]
            if i[0] not in listanod:
                S.add_node(i[0], pos=[nodoos.loc[i[0]]["x"],nodoos.loc[i[0]]["y"]], index=i[0])
                listanod.append(i[0])
            if i[1] not in listanod:
                S.add_node(i[1], pos=[nodoos.loc[i[1]]["x"],nodoos.loc[i[1]]["y"]], index=i[1])
                listanod.append(i[1])    
            if oneway==True:
                #l=0
                S.add_edge(i[0],i[1], fcosto=f1, flujo=0, costo=0, color=color, nombre=nombre_e, w=linew, L_atri=L_atr, p_atri=p_atr, u_atri=u_atr, v_atri=v_atr)
            else:
                S.add_edge(i[0],i[1], fcosto=f1, flujo=0, costo=0, color=color, nombre=nombre_e, w=linew, L_atri=L_atr, p_atri=p_atr, u_atri=u_atr, v_atri=v_atr)
                #S.add_edge(i[1],i[0], fcosto=f1, flujo=0, costo=0, color=color, nombre=nombre_e, w=linew, L_atri=L_atr, p_atri=p_atr, u_atri=u_atr, v_atri=v_atr)
        #a=1
S.add_edge(514090676,253251270, fcosto=f1, flujo=0, costo=0, color="yellow", nombre="link", w=1, L_atri=5, p_atri=1, u_atri=3, v_atri=15)        
S.add_edge(4441169826,240427952, fcosto=f1, flujo=0, costo=0, color="yellow", nombre="link", w=1, L_atri=5, p_atri=1, u_atri=3, v_atri=15) 
def costox(ni,nf,attr):
    funcosto_arco=attr["fcosto"]
    q_arco=attr["flujo"]/5400
    p_arco=attr["p_atri"]
    L_arco=attr["L_atri"]
    v_arco=attr["v_atri"]
    u_arco=attr["u_atri"]
    return (funcosto_arco(q_arco, p_arco, L_arco, v_arco, u_arco))
#print(nodoos.loc[4441169826])
labels = nx.get_edge_attributes(S,"nombre")
#labelsnodoindex = nx.get_node_attributes(S,"index")
#print(labelsnodoindex)
#if 14805063 in listaidnodos: print("yes")
colors = []
widths = []
#for i in S.edges: print(i)

for ni, nf in S.edges:
    colors.append(S.edges[ni,nf]["color"])
    widths.append(S.edges[ni,nf]["w"])
#for i in S.edges:
#    colors.append(S.edges[i]["color"])
pos = nx.get_node_attributes(S,"pos")
plt.figure()
ax=plt.subplot(111)
zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")
#zonas_seleccionadas2.plot(ax=ax, color="#FFB2B2")
nx.draw_networkx_nodes(S, pos=pos, node_size=3)
#nx.draw_networkx_nodes(S, pos=pos, node_size=12)
nx.draw_networkx_labels(S, pos=pos,font_size=12)#
#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, font_size=10)#
#print(a)
diccionario_nodorepresentativo={}
nx.draw_networkx_edges(S, pos, edge_color=colors, width=widths)

for idx,row in zonas_seleccionadas.iterrows(): 
    distancia_actual = np.infty
    #print(row["ID"], idx)
    c=row.geometry.centroid
    cx_zona=c.x
    cy_zona=c.y
    #print(c.x,c.y)
    ax.annotate(text=row["ID"], xy=(c.x,c.y), horizontalalignment="center", color="magenta")

    for i, node in enumerate(S.nodes):
        #print(G.nodes[node])
        #print(node)
        cx_nodo=(S.nodes[node]["pos"][0])
        cy_nodo=(S.nodes[node]["pos"][1])
        #print(S.nodes[node]["index"])
        dist_nodo=np.sqrt((cx_nodo-cx_zona)**2 +(cy_nodo-cy_zona)**2)
        if dist_nodo<distancia_actual:
            distancia_actual=dist_nodo
            nodo_cercano=node
            diccionario_nodorepresentativo[row["ID"]]=nodo_cercano
#print(diccionario_nodorepresentativo)
nuevodic={}
for key in DiccionarioMatrizOD:
    A=diccionario_nodorepresentativo[key[0]]
    B=diccionario_nodorepresentativo[key[1]]
    nuevodic[A,B]=float(DiccionarioMatrizOD[key])
#print(DiccionarioMatrizOD) 
#print(nuevodic) 
#print(patata)

centroides_seleccionados.plot(ax=ax, marker="o", color="magenta", markersize=8)
plt.show()
OD=nuevodic
OD_target=OD.copy()
while True:
    se_asigno_demanda=False
    for key in OD:
        demanda_actual = OD[key]
        demanda_objetivo=OD_target[key]

        if demanda_actual>0:
            
            path=dijkstra_path(S,key[0],key[1], weight=costox)
            #incrementar flujo en ruta minima
            Nparadas =len(path)
            
            for i_parada in range(Nparadas-1):
                o=path[i_parada]
                d= path[i_parada+1]
                flujo_antes=S.edges[o,d]["flujo"]

                S.edges[o,d]["flujo"]+=OD_target[key]/10
                #print(OD_target[key]/1000)
            OD[key]-=OD_target[key]/10
            se_asigno_demanda=True
    if not se_asigno_demanda: break
#S.add_edge("A","B", fcosto=0, flujo=0, costo=0)#r
#print(nodoos.loc[4464991880])
for ni,nf in S.edges:
    arco =S.edges[ni,nf]
    funcosto_arco=arco["fcosto"]
    q_arco=arco["flujo"]/5400
    p_arco=arco["p_atri"]
    L_arco=arco["L_atri"]
    v_arco=arco["v_atri"]
    u_arco=arco["u_atri"]
    arco["costo"]=funcosto_arco(q_arco, p_arco, L_arco, v_arco, u_arco)
#398.1,687.03176715

plt.figure()
ax=plt.subplot(111)
zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")

nx.draw_networkx_nodes(S, pos=pos, node_size=3)
for idx,row in zonas_seleccionadas.iterrows(): 
    distancia_actual = np.infty
    #print(row["ID"], idx)
    c=row.geometry.centroid
    cx_zona=c.x
    cy_zona=c.y
    #print(c.x,c.y)
    ax.annotate(text=row["ID"], xy=(c.x,c.y), horizontalalignment="center", color="magenta")
nx.draw_networkx_edges(S, pos, edge_color=colors, width=widths)
labels = nx.get_edge_attributes(S,"flujo")
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, font_size=10)
plt.show()

costored=0
for ni,nf in S.edges:
    arco =S.edges[ni,nf]
    costored+=arco["costo"]
print(f"Costo total en la red = {costored}")

