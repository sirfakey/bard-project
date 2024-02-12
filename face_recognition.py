from audio_recorder_streamlit import audio_recorder
from deepface import DeepFace
import streamlit as st
import os
from audiorecorder import audiorecorder
import whisper
import re
import openai


prompt = None


base_model = whisper.load_model('base')
openai.api_key = "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"

# You are Freya, an AI chatbot designed to assist students in their learning journey. You are equipped with the ability to understand students' grade levels, emotions, and names, tailoring your responses to provide personalized and helpful interactions. Your primary goal is to enhance students' understanding of various subjects, offer academic support, and create a positive and engaging learning experience. You can help with answering questions, explaining concepts, giving feedback, and providing encouragement. Remember to be friendly, patient, and adaptive in your conversations, ensuring that students feel supported and empowered in their studies. Don't use markdown, and don't use emojis.

token = 'ZgiXs83PvL_oThtEb185bFzrfHqu8qch0x5mU3TtRzMu1FvX9Hrv6XWLyi__T2E2_fPorw.'

with st.sidebar.expander("**About**"):
    st.write('Freya is an interactive voice assistant based on Bard by Google. Freya was designed to help students of all classes.')
    st.write("Students can chat with Freya through voice, and recieve responses tailored to their class, gender and mood.")
    st.write("**Developed and designed by Arghya Biswas, SM Mahdin and with the help of our ICT teacher, Shariff sir.**")


with st.sidebar.expander("**Personal information**"):
    cls = st.selectbox("2", ('grade 12', 'grade 11', 'grade 10', 'grade 9', 'grade 8', "grade 7", "grade 6",
                       "grade 5", "grade 4", " grade 3", "grade 2", "grade 1", ), placeholder="Class", label_visibility="hidden")
    name = st.text_input("Your name :")

student_grade = cls

with st.sidebar.expander("**Your gender and emotion**"):
    image_buffer = st.camera_input("")

    if image_buffer:
        with open(os.path.join("tempDir", "image.png"), "wb") as f:
            f.write(image_buffer.getbuffer())
    result = DeepFace.analyze(img_path="tempDir/image.png")

gender = result[0]["dominant_gender"]
emotion = result[0]["dominant_emotion"]

st.sidebar.write("Gender :", gender, "Emotion :", emotion)

with st.sidebar.expander("**Settings**"):
    stt = st.select_slider(
        "1", ("No speech to text", "Speech to text"), label_visibility="hidden")
    tts = st.select_slider(
        "2", ("Text to Speech", "No Text to Speech"), label_visibility="hidden")
    if tts == "Text to Speech":
        voicespeed = st.slider("Pick TTS voice speed", 1.5, 5.0)
    reset_mood = st.button("Reset Chat Mood")

audio_bytes = None
prompt_text = None

if reset_mood == True:
    audio = None
    prompt_text = None
    st.experimental_rerun


if stt == "Speech to text":
    if not 'audio' in st.session_state:
        st.session_state.audio = None
    with st.expander("**Push To Talk**"):
        st.session_state.audio = audio_recorder(
            text="",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="2x",
        )

if stt == "Speech to text":
    if st.session_state.audio:
        with open("foo1.wav", "wb") as f:
            f.write(st.session_state.audio)
    result1 = base_model.transcribe('foo1.wav')
    prompt_text = result1['text']
    prompt = prompt_text
    st.session_state.audio = None
    if prompt:

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"
        if "messages" not in st.session_state:
            st.session_state.messages = []

        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append(
            {"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            messages_for_openai = [
                {"role": "system", "content": "You are Freya, an AI chatbot designed to assist students in their learning journey. You are equipped with the ability to understand students' grade levels, emotions, and names, tailoring your responses to provide personalized and helpful interactions. Your primary goal is to enhance students' understanding of various subjects, offer academic support, and create a positive and engaging learning experience. You can help with answering questions, explaining concepts, giving feedback, and providing encouragement. Remember to be friendly, patient, and adaptive in your conversations, ensuring that students feel supported and empowered in their studies. Don't use markdown, and don't use emojis. They have the emotion of " + emotion + ", in" + student_grade + ", their name is" + name + ", thay are a" + gender + ". Try to keep it under 40 words. Keep it as concise as possible."}
            ]
            for m in st.session_state.messages:
                new_message = {"role": m["role"], "content": m["content"]}
                messages_for_openai.append(new_message)

            for response in openai.ChatCompletion.create(
                model=st.session_state.openai_model,
                messages=messages_for_openai,
                stream=True,
            ):
                full_response += response.choices[0].delta.get(
                    "content", "")
            message_placeholder.markdown(full_response)

elif stt == "No speech to text":
    prompt = st.chat_input("Ask away!")

if stt == "No speech to text":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Construct the messages_for_openai list using a loop
            messages_for_openai = [
                {"role": "system", "content": "You are Freya, an AI chatbot designed to assist students in their learning journey. You are equipped with the ability to understand students' grade levels, emotions, and names, tailoring your responses to provide personalized and helpful interactions. Your primary goal is to enhance students' understanding of various subjects, offer academic support, and create a positive and engaging learning experience. You can help with answering questions, explaining concepts, giving feedback, and providing encouragement. Remember to be friendly, patient, and adaptive in your conversations, ensuring that students feel supported and empowered in their studies. Don't use markdown, and don't use emojis. They have the emotion of " + emotion + ", in" + student_grade + ", their name is" + name + ", thay are a" + gender + ". Try to keep it under 40 words. Keep it as concise as possible."}
            ]
            for m in st.session_state.messages:
                new_message = {"role": m["role"], "content": m["content"]}
                messages_for_openai.append(new_message)

            for response in openai.ChatCompletion.create(
                model=st.session_state.openai_model,
                messages=messages_for_openai,
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response})


def generate_voice(text, voice, voice_speed):
    js_code = f"""
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance("{text}");
        utterance.voice = speechSynthesis.getVoices().filter((v) => v.name === "{voice}")[0];
        utterance.rate = {voice_speed};
        utterance.volume = 1;
        synth.speak(utterance);
    """
    st.components.v1.html(f"<script>{js_code}</script>", height=0)


bard_response = None

if prompt:
    bard_response = full_response
    spokenResponse = re.sub(r'\s+', ' ', bard_response)
    spokenResponse = spokenResponse.lstrip().rstrip()
    spokenResponse = spokenResponse.replace('"', " ").replace("-", " ")
# Easter eggs

if prompt == "HappY BirthdaY":
    with st.chat_message('assistant', avatar="🤖"):
        video_file = open('tempDir/happy_birthday.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
elif prompt == "Arghya is gay":
    video_file = open('tempDir/arghaya.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

if tts == "Text to Speech":
    if bard_response:
        generate_voice(spokenResponse, "Google italiano", voicespeed)
