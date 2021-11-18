import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gps
zonas_gdf = gps.read_file("eod.json")
ox.config(use_cache=True, log_console=True)
#zonass=[18,12,17,19,13,20,49,50,48]
zonass=[146,590,506,683,682,666,684,677,306,287,307,288,291,289,290,304,266]
zonas_seleccionadas=zonas_gdf[zonas_gdf["ID"].isin(zonass)] #Centro + bordes
north=-33.34
west=-70.645
south=-33.445
east=-70.555
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
    clean_periphery=True)

a,b=ox.graph_to_gdfs(G)
plt.figure()
ax=plt.subplot(111)
zonas_seleccionadas.plot(ax=ax)
plt.show()




gdf_nodes,gdf_edges = ox.graph_to_gdfs(G)
street_centroids=gdf_edges.centroid

plt.figure()
ax=plt.subplot(111)
zonas_seleccionadas2=zonas_gdf[zonas_gdf["ID"].isin([146])] #Centro

centroides_seleccionados=zonas_seleccionadas.centroid

cont=0
gdf_nodes=gps.clip(gdf_nodes, zonas_seleccionadas)    
for idx,row in zonas_seleccionadas.iterrows(): 
    #print(row["ID"], idx)
    c=row.geometry.centroid
    ax.annotate(text=row["ID"], xy=(c.x,c.y), horizontalalignment="center")
zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")
zonas_seleccionadas2.plot(ax=ax, color="#FFB2B2")
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
posibles=["motorway","secondary","tertiary","primary","residential"]
#posibles=["secondary","tertiary"]
#for i in listaidedges:
    #if gdf_edges.loc[i]["highway"] in posibles:
        
        #S.add_edge(i[0],i[1], fcosto=0, flujo=0, costo=0)
        #print("ayoo")
S=nx.DiGraph()
for i in clipn:
    S.add_node(i, pos=[nodoos.loc[i]["x"],nodoos.loc[i]["y"]], index=i)
for i in listaidedges:
    tipo=gdf_edges.loc[i]["highway"]
    nombre_e=gdf_edges.loc[i]["name"]
    if i[0] in clipn and i[1] in clipn:
        if tipo=="motorway": color="orange"#red
        elif tipo=="secondary": color="green"#yellow
        elif tipo=="tertiary": color="blue"#blue
        elif tipo=="primary": color="yellow"#green
        #elif tipo=="residential": color="black"#black
        else: tipo=""
        if tipo!="":
            oneway=gdf_edges.loc[i]["oneway"]
            if oneway==True:
                #l=0
                S.add_edge(i[0],i[1], fcosto=0, flujo=0, costo=0, color=color, nombre=nombre_e)
            else:
                S.add_edge(i[0],i[1], fcosto=0, flujo=0, costo=0, color=color, nombre=nombre_e)
                S.add_edge(i[1],i[0], fcosto=0, flujo=0, costo=0, color=color, nombre=nombre_e)
        #a=1
labels = nx.get_edge_attributes(S,"nombre")
#labelsnodoindex = nx.get_node_attributes(S,"index")
#print(labelsnodoindex)
#if 14805063 in listaidnodos: print("yes")
colors = []
for ni, nf in S.edges:
    colors.append(S.edges[ni,nf]["color"])

pos = nx.get_node_attributes(S,"pos")
plt.figure()
ax=plt.subplot(111)
zonas_seleccionadas.plot(ax=ax, color="#CDCDCD")
zonas_seleccionadas2.plot(ax=ax, color="#FFB2B2")
#nx.draw_networkx_nodes(S, pos=pos, node_size=3)
#nx.draw_networkx_nodes(S, pos=pos, node_size=9)
#nx.draw_networkx_labels(S, pos=pos,font_size=12)#
#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, font_size=10)#
#print(a)
nx.draw_networkx_edges(S, pos, edge_color=colors)
for idx,row in zonas_seleccionadas.iterrows(): 
    #print(row["ID"], idx)
    c=row.geometry.centroid
    ax.annotate(text=row["ID"], xy=(c.x,c.y), horizontalalignment="center")
plt.show()

#S.add_edge("A","B", fcosto=0, flujo=0, costo=0)#r
#print(nodoos.loc[4464991880])