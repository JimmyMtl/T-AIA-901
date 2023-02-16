import streamlit as st
import speech_recognition as sr
import soundfile
from pydub import AudioSegment

r = sr.Recognizer()

listening = False
strlistening = "Recording" if listening else "Talk"

uploaded_file = st.file_uploader("Glissez votre fichier audio (mp3, flac ou wav)", ["mp3", "flac", "wav"])


def start_recognition():
    with sr.Microphone() as source2:
        # st.write("Listen")
        # audio = r.listen(source2)
        # st.write("Enregistrement")
        # with open("bonjour-je-suis-john.wav","wb") as file:
        #    file.write(audio.get_wav_data())
        # st.write("Enregistré")

        st.write("Start Recognition")
        r.adjust_for_ambient_noise(source2, duration=1)
        st.write("You can talk")
        audio = r.listen(source2)

        st.write("Analyzing audio")

        try:
            MyText = r.recognize_google(audio, None, "fr-FR")
            st.write("Vous avez dit : " + MyText.lower())
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.write("Could not request results from Google Speech Recognition service; {0}".format(e))


def start_recognition_with_file():
    file_from_upload = uploaded_file
    if uploaded_file.name.endswith('.mp3'):
        st.write('convert mp3 file')
        mp3data = AudioSegment.from_mp3(file_from_upload)
        file_from_upload.name = file_from_upload.name.replace('.mp3', '.wav')
        mp3data.export('temp.wav', format='wav')
    else:
        st.write('work with wav file')
        basedata, basesamplerate = soundfile.read(uploaded_file)
        soundfile.write(f'temp.wav', basedata, basesamplerate, subtype='PCM_16')

    with sr.AudioFile(f"temp.wav") as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.record(source)
        # st.write('ok')
        try:
            MyText = r.recognize_google(audio, None, "fr-FR")
            st.write("Vous avez dit : " + MyText.lower())
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.write("Could not request results from Google Speech Recognition service; {0}".format(e))


#     st.write("Analyzing audio")


if st.button(strlistening):
    start_recognition()

if uploaded_file is not None:
    if st.button("Analyze file"):
        start_recognition_with_file()
