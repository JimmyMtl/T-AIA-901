import json
import math
import time
import pandas as pd
import streamlit as st


def getCoordinates(gare):
    dfStop = pd.read_csv('../data_sncf/stops.txt', sep=",")
    dfGare = dfStop[dfStop['stop_name'] == gare]
    latitude = dfGare['stop_lat'].values[0]
    longitude = dfGare['stop_lon'].values[0]
    tab = [float(latitude), float(longitude)]
    return tab


def getShortestPath(start, end, graph):
    unvisited = graph
    shortest_distances = {}
    route = []
    path_nodes = {}

    for nodes in unvisited:
        shortest_distances[nodes] = math.inf
    shortest_distances[start] = 0

    while unvisited:
        min_node = None
        for current_node in unvisited:
            if min_node is None:
                min_node = current_node
            elif shortest_distances[min_node] \
                    > shortest_distances[current_node]:
                min_node = current_node
        for (node, value) in unvisited[min_node].items():
            if value + shortest_distances[min_node] \
                    < shortest_distances[node]:
                shortest_distances[node] = value \
                    + shortest_distances[min_node]
                path_nodes[node] = min_node
        unvisited.pop(min_node)
    node = end

    while node != start:
        try:
            route.insert(0, node)
            node = path_nodes[node]
        except Exception:
            print('Path not reachable')
            break
    route.insert(0, start)

    if shortest_distances[end] != math.inf:
        st.write('Le trajet va durer ' + time.strftime('%H:%M:%S',
                                                       time.gmtime(shortest_distances[end])))

        lat = []
        lon = []

        for i in route:
            coord = getCoordinates(i)
            lat.append(coord[0])
            lon.append(coord[1])

        position = pd.DataFrame({'lat': lat, 'lon': lon})

        st.write('Voici vos', len(route), 'arrêts:')
        st.write(' -> '.join(route))

        st.map(position)


st.title('Travel Order')
st.write("Veuillez entrer les gares de départ et d'arrivée")
start = st.text_input("Gare de départ")
end = st.text_input("Gare d'arrivée")
if st.button("Calculer"):
    getShortestPath(start, end, json.loads(
        open("./graph.json", "r").read()))
