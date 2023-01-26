import json
import math
import time
import pandas as pd
import streamlit as st
import spacy
import speech_recognition as sr

# initialisation de la reconnaissance vocale
r = sr.Recognizer()
listening = False
strlistening = "Enregistrement.." if listening else "Parler"


# Fonction de reconnaissance vocale
def start_recognition():
    with sr.Microphone() as source2:
        st.write("Démarage de la reconnaissance vocale")
        r.adjust_for_ambient_noise(source2, duration=1)
        st.write("Vous pouvez parler")
        audio = r.listen(source2)

        st.write("Analyse de l'audio")

        try:
            MyText = r.recognize_google(audio, None, "fr-FR")
            st.write("Vous avez dit : " + MyText.lower())
            return MyText
        except sr.UnknownValueError:
            st.write("La phrase n'a pas été comprise")
        except sr.RequestError as e:
            st.write(
                "Impossible de se connecter au service Google Speech Recognition; {0}".format(e))

# Fonction de récupération des coordonnées GPS d'une gare
def getCoordinates(gare):
    dfStop = pd.read_csv('shortestPath/sncf/stops.txt', sep=",")
    dfGare = dfStop[dfStop['stop_name'] == gare]
    latitude = dfGare['stop_lat'].values[0]
    longitude = dfGare['stop_lon'].values[0]
    tab = [float(latitude), float(longitude)]
    return tab

# Fonction de récupération du nom d'une gare à partir d'une ville
def get_gare_name(ville):
    dfStop = pd.read_csv('shortestPath/sncf/stops.txt', sep=",")
    dfGare = dfStop[dfStop['stop_id'].str.contains('StopPoint:OCETrain')]
    gare = dfGare[dfGare['stop_name'].str.contains(
        'Gare de ' + ville)]['stop_name'].values[0]
    return gare

# Fonction d'extraction des villes de départ et d'arrivée
def extract_dep_and_arr(txt):
    ner = spacy.load('NLP/Spacy/model_ner')
    doc = ner(txt)

    for ent in doc.ents:
        if ent.label_ == 'DEP':
            dep = ent.text
        if ent.label_ == 'ARR':
            arr = ent.text

    try:
        dep = get_gare_name(dep)
        arr = get_gare_name(arr)
    except Exception:
        dep = None
        arr = None

    return dep,arr

# Fonction de calcul du trajet le plus court
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


# Interface Streamlit
st.title('Travel Order')

if st.button(strlistening):
    phrase = start_recognition()
    # st.write(phrase)

    dep, arr = extract_dep_and_arr(phrase)

    if dep is None or arr is None:
        st.write("Impossible de trouver les villes de départ et d'arrivée. Il semble qu'il n'y ait pas de villes dans votre phrase.")
    else:
        st.write('Vous souhaitez partir de', dep, 'et arrivez à', arr)

        getShortestPath(dep, arr, json.loads(
            open("shortestPath/graph.json", "r").read()))