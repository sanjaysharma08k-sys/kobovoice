import streamlit as st
import tempfile
import os
from gradio_client import Client, handle_file

st.set_page_config(page_title="Mera Voice Cloner", page_icon="🎙️")
st.title("🎙️ Mera Permanent Voice Cloner")
st.write("Text likho, teri hi voice me awaaz ban jayegi. Ab ye halka wala hai, error nahi aayega.")

text = st.text_area("Yahan Text Likho - Jo Bolwana Hai", "Namaste dosto, ye meri cloned voice hai.", height=120)
language = st.radio("Language Chunno", ["hi", "en"], index=0)
voice_file = st.file_uploader("Apni Voice Upload Karo (10 sec ki)", type=["mp3", "wav"])

if st.button("🔊 Bolo - Awaaz Banao"):
    if not text.strip():
        st.warning("Pehle text likho!")
    elif voice_file is None:
        st.warning("Pehle apni voice wali file upload karo!")
    else:
        with st.spinner("Awaaz ban rahi hai... 20-30 sec wait karo"):
            try:
                # Voice file ko temp me save karo
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tmp.write(voice_file.read())
                    tmp_path = tmp.name
                # Public XTTS Space ko call karo - model wahan chalega
                client = Client("coqui/xtts")
                result = client.predict(
                    text=text,
                    language=language,
                    speaker_audio=handle_file(tmp_path),
                    api_name="/generate"
                )
                st.success("Ho gaya!")
                st.audio(result)
                with open(result, "rb") as f:
                    st.download_button("Download Karo", f, file_name="output.wav")
                os.unlink(tmp_path)
            except Exception as e:
                st.error(f"Error aa gaya: {e}")
                st.info("Dobara try karo, kabhi-kabhi server busy hota hai")
