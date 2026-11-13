import streamlit as st
from TTS.api import TTS

st.set_page_config(page_title="Mera Voice Cloner", page_icon="🎙️")
st.title("🎙️ Mera Permanent Voice Cloner")
st.write("Text likho, teri hi voice me awaaz ban jayegi.")

text = st.text_area("Yahan Text Likho - Jo Bolwana Hai", "Namaste dosto, ye meri cloned voice hai.", height=120)
language = st.radio("Language Chunno", ["hi", "en"], index=0, help="hi = Hindi, en = English")

if st.button("🔊 Bolo - Awaaz Banao"):
    if not text.strip():
        st.warning("Pehle text likho!")
    else:
        with st.spinner("Awaaz ban rahi hai... thoda wait karo 30 sec"):
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
            tts.tts_to_file(
                text=text,
                speaker_wav="meri_voice.wav",
                language=language,
                file_path="output.wav"
            )
            st.success("Ho gaya!")
            st.audio("output.wav")
            with open("output.wav", "rb") as f:
                st.download_button("Download Karo", f, file_name="output.wav")
