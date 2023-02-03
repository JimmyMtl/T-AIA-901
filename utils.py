import spacy
import speech_recognition as sr
from pydub import AudioSegment
import soundfile
import math
import time
import pandas as pd
import streamlit as st
import os


def start_recognition():
    with st.spinner('I\'m listening to you...'):
        # initialisation de la reconnaissance vocale
        r = sr.Recognizer()
        with sr.Microphone() as source2:
            st.write("Démarage de la reconnaissance vocale")
            r.adjust_for_ambient_noise(source2, duration=1)
            st.write("Vous pouvez parler")
            audio = r.listen(source2)
            st.write("Analyse de l'audio")
            try:
                MyText = r.recognize_google(audio, None, "fr-FR")
                st.write("Vous avez dit : ")
                st.success(MyText.lower())
                return MyText
            except sr.UnknownValueError:
                st.error("La phrase n'a pas été comprise")
            except sr.RequestError as e:
                st.error(
                    "Impossible de se connecter au service Google Speech Recognition; {0}".format(e))


def start_recognition_with_file(uploaded_file):
    with st.spinner('Chargement...'):

        file_from_upload = uploaded_file
        if uploaded_file.name.endswith('.mp3'):
            mp3data = AudioSegment.from_mp3(file_from_upload)
            file_from_upload.name = file_from_upload.name.replace('.mp3', '.wav')
            mp3data.export('temp.wav', format='wav')
        else:
            basedata, basesamplerate = soundfile.read(uploaded_file)
            soundfile.write(f'temp.wav', basedata, basesamplerate, subtype='PCM_16')

        mytext = ""
        with sr.AudioFile(f"temp.wav") as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.record(source)
            try:
                mytext = r.recognize_google(audio, None, "fr-FR")
            except sr.UnknownValueError:
                st.error("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                st.error("Could not request results from Google Speech Recognition service; {0}".format(e))
        try:
            os.remove("temp.wav")
        except Exception:
            pass
        return mytext


# Fonction de récupération des coordonnées GPS d'une gare
def getCoordinates(gare):
    dfStop = pd.read_csv('data_sncf/stops.txt', sep=",")
    dfGare = dfStop[dfStop['stop_name'] == gare]
    latitude = dfGare['stop_lat'].values[0]
    longitude = dfGare['stop_lon'].values[0]
    tab = [float(latitude), float(longitude)]
    return tab


# Fonction de récupération du nom d'une gare à partir d'une ville
def get_gare_name(ville):
    dfStop = pd.read_csv('data_sncf/stops.txt', sep=",")
    dfGare = dfStop[dfStop['stop_id'].str.contains('StopPoint:OCETrain')]
    gare = dfGare[dfGare['stop_name'].str.contains(
        'Gare de ' + ville)]['stop_name'].values[0]
    return gare


# Fonction d'extraction des villes de départ et d'arrivée
def extract_dep_and_arr(txt):
    ner = spacy.load('model_ner')
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

    return dep, arr


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
        listle = ' - '.join(route)
        print(route)
        st.write("| Departure | Arrival |")
        st.write("| --- | --- |")
        for index, i in enumerate(route):
            print(i, index)
            if index < len(route) - 1:
                st.write(f'| {i} | {route[index + 1]} |')

        st.map(position)
