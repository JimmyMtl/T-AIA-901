import json
import streamlit as st
from utils import start_recognition, \
    start_recognition_with_file, \
    getShortestPath, \
    extract_dep_and_arr, \
    get_gare_name, \
    getCoordinates

st.title('Welcome to Travel Order')
st.subheader('Please press start then talk to get your route')
listening = False
strlistening = "Analyzing your text.." if listening else "Start talking"

# Interface Streamlit
if st.button(strlistening):
    phrase = start_recognition()
    with st.spinner('Loading..'):
        if phrase:
            dep, arr = extract_dep_and_arr(phrase)

            if dep is None or arr is None:
                st.write(
                    "Cannot find a city departure and/or arrival. It seems that there is no city in your sentence")
            else:
                st.write('Vous souhaitez partir de', dep, 'et arrivez à', arr)

                getShortestPath(dep, arr, json.loads(
                    open("gareGraph/graph.json", "r").read()))

st.text('or you can provide some audio file')
uploaded_file = st.file_uploader("Glissez votre fichier audio (mp3, flac ou wav)", ["mp3", "flac", "wav"])

if uploaded_file is not None:
    phrase = start_recognition_with_file(uploaded_file)
    st.write('You said :', phrase)
    with st.spinner('Loading..'):
        if phrase:
            dep, arr = extract_dep_and_arr(phrase)

            if dep is None or arr is None:
                st.error(
                    "Cannot find a city departure and/or arrival. It seems that there is no city in your sentence")
            else:
                st.write('Vous souhaitez partir de', dep, 'et arrivez à', arr)

                getShortestPath(dep, arr, json.loads(
                    open("shortestPath/graph.json", "r").read()))
