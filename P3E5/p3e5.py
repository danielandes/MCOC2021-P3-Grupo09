import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gps
import pandas
zonas_gdf = gps.read_file("eod.json")
ox.config(use_cache=True, log_console=True)
#zonass=[18,12,17,19,13,20,49,50,48]
zonass=[146,590,683,682,666,684,677,306,287,307,288,291,289,290,304,266,434,269,267,281,435,147,148,145,153,598,597,599,587,678,667,669,508,507,496,505,512,504,305,291,307,320,306,668,292,433,432,509,282,283,284,426.579,144,578,143,88,89,87,92,95,94,93,151,579,426,440,278,280,279,439,438,442,436,471]
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
    if ni in zonass and nf in zonass:
        DiccionarioMatrizOD[(ni,nf)]=valor
print(DiccionarioMatrizOD) 
print(len(DiccionarioMatrizOD)) 
    #print(datoseod.loc[i]["398"],datoseod.loc[i]["398.1"],datoseod.loc[i]["687.03176715"])


gdf_nodes,gdf_edges = ox.graph_to_gdfs(G)
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
#for i in clipn:
#    S.add_node(i, pos=[nodoos.loc[i]["x"],nodoos.loc[i]["y"]], index=i)
for i in listaidedges:
    if i[0] in clipn and i[1] in clipn:
        tipo=gdf_edges.loc[i]["highway"]
        nombre_e=gdf_edges.loc[i]["name"]
    #
    #
        linew=1
        if tipo=="motorway": color="orange"#red
        elif tipo=="secondary": color="green"#yellow
        elif tipo=="tertiary": color="blue"#blue
        elif tipo=="primary": color="yellow"#green
        elif tipo=="construction": 
            #print("aha",gdf_edges.loc[i]["highway"],gdf_edges.loc[i]["name"])
            color="red" 
            linew=6
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
                S.add_edge(i[0],i[1], fcosto=0, flujo=0, costo=0, color=color, nombre=nombre_e, w=linew)
            else:
                S.add_edge(i[0],i[1], fcosto=0, flujo=0, costo=0, color=color, nombre=nombre_e, w=linew)
                S.add_edge(i[1],i[0], fcosto=0, flujo=0, costo=0, color=color, nombre=nombre_e, w=linew)
        #a=1
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
#nx.draw_networkx_nodes(S, pos=pos, node_size=3)
#nx.draw_networkx_nodes(S, pos=pos, node_size=12)
#nx.draw_networkx_labels(S, pos=pos,font_size=12)#
#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, font_size=10)#
#print(a)
nx.draw_networkx_edges(S, pos, edge_color=colors, width=widths)
#for idx,row in zonas_seleccionadas.iterrows(): 
    #print(row["ID"], idx)
    #c=row.geometry.centroid
    #ax.annotate(text=row["ID"], xy=(c.x,c.y), horizontalalignment="center", color="magenta")
centroides_seleccionados.plot(ax=ax, marker="o", color="magenta", markersize=8)
plt.show()

#S.add_edge("A","B", fcosto=0, flujo=0, costo=0)#r
#print(nodoos.loc[4464991880])

#398.1,687.03176715