import streamlit as st
import pandas as pd
import os
import io
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from st_audiorec import st_audiorec

# Constants
METADATA_PATH = os.path.join("data", "metadata.csv")
OUTPUT_DIR = os.path.join("data", "tts", "wavs")

# Load metadata
@st.cache_data
def load_metadata():
    df = pd.read_csv(METADATA_PATH, sep="|", header=None, names=["filename", "transcript", "extra"])
    return df[["filename", "transcript"]]

df = load_metadata()

# Auto-advance to first unrecorded line
existing_files = set(f for f in os.listdir(OUTPUT_DIR) if f.endswith(".wav"))
first_missing_index = next((i for i, row in df.iterrows()
                            if f"{row.filename}.wav" not in existing_files), len(df) - 1)

if "current_index" not in st.session_state:
    st.session_state.current_index = first_missing_index

# App title
st.title("🎤 Voice Recorder for TTS Dataset")

# Progress display
completed = len(existing_files)
total = len(df)
st.markdown(f"**Progress: {completed}/{total} lines recorded**")
st.progress(completed / total)

# Navigation controls
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("⬅️ Back", use_container_width=True) and st.session_state.current_index > 0:
        st.session_state.current_index -= 1
        st.rerun()

with col2:
    if st.button("➡️ Forward", use_container_width=True) and st.session_state.current_index + 1 < total:
        st.session_state.current_index += 1
        st.rerun()



# Current row
row = df.iloc[st.session_state.current_index]
st.markdown(f"**Line {st.session_state.current_index + 1}/{total} to record**")
st.markdown("**Transcript:**")
st.text_area("", row.transcript, height=100)

# Record audio
wav_audio_data = st_audiorec()

# Trim silence
def trim_silence(audio_bytes):
    sound = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
    nonsilent = detect_nonsilent(sound, min_silence_len=300, silence_thresh=-40)
    if not nonsilent:
        return None
    start_trim = nonsilent[0][0]
    end_trim = nonsilent[-1][1]
    trimmed = sound[start_trim:end_trim]
    trimmed_bytes = io.BytesIO()
    trimmed.export(trimmed_bytes, format="wav")
    trimmed_bytes.seek(0)
    return trimmed_bytes

# Handle audio result
if wav_audio_data:
    trimmed_audio = trim_silence(wav_audio_data)
    if trimmed_audio:
        st.session_state.trimmed_audio = trimmed_audio
        st.session_state.ready_to_save = True
    else:
        st.error("Silence-only recording. Try again.")

# Save recording and auto-advance
if st.session_state.get("ready_to_save"):
    if st.button("💾 Save Recording"):
        save_path = os.path.join(OUTPUT_DIR, f"{row.filename}.wav")
        with open(save_path, "wb") as f:
            f.write(st.session_state.trimmed_audio.read())

        st.toast(f"✅ Saved: {row.filename}.wav")

        # Reset state
        st.session_state.ready_to_save = False
        st.session_state.trimmed_audio = None
        st.session_state["_uploaded_file_mgr"] = {}
        st.session_state["_widget_state"] = {}

        # Advance to next line
        if st.session_state.current_index + 1 < total:
            st.session_state.current_index += 1
        else:
            st.info("🎉 All lines completed!")

        st.rerun()
