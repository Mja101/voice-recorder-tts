# 🎤 Voice Recorder for TTS Dataset

A Streamlit-based web app that enables users to record, trim, and save high-quality voice samples for Text-to-Speech (TTS) datasets. Automatically tracks progress and ensures consistent file naming from a predefined transcript file.

---

## Features

-  **Transcript Navigation**  
  Automatically resumes from the first missing line and supports manual back/forward navigation.

-  **Inline Recording Interface**  
  Built-in recorder using `st_audiorec`, no need for external tools.

-  **Silence Trimming**  
  Automatically trims leading and trailing silence from recordings using PyDub.

-  **Auto Save & Progress Tracking**  
  Saves recordings to disk and updates progress in real time.

-  **User Feedback**  
  Toast notifications confirm successful saves.

---

## Directory Structure

```
project-root/
├── app.py                 # Main Streamlit app
├── data/
│   ├── metadata.csv       # CSV with transcripts and filenames
│   └── tts/
│       └── wavs/          # Output directory for saved recordings
```

---

## Transcript Format (`metadata.csv`)

Expected format is pipe-delimited (`|`) with the following structure:

```
filename|transcript|extra
LJ001-0001|This is an example line to read aloud.|
LJ001-0002|Another line for recording.|
...
```

Only the `filename` and `transcript` columns are used.

---

## Setup Instructions

1. **Install dependencies**  
   Ensure you have Python 3.8+ and install the required packages:

   ```bash
   pip install streamlit pandas pydub soundfile st_audiorec
   ```

   You may also need `ffmpeg` installed on your system (required by PyDub):

   ```bash
   # Ubuntu
   sudo apt install ffmpeg

   # MacOS
   brew install ffmpeg

   # Windows
   winget install "FFmpeg (Essentials Build)"
   ```



2. **Prepare your dataset**  
   - Add `metadata.csv` to the `data/` directory.
   - Ensure each transcript line has a unique filename.

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## How to Use

1. The app starts at the first unrecorded line.
2. Press **Start Recording**, then **Stop** when finished.
3. Press **💾 Save Recording** to:
   - Trim silence
   - Save the `.wav` file to `data/tts/wavs/`
   - Automatically move to the next line
4. Use the ⬅️ **Back** or ➡️ **Forward** buttons to navigate manually.
5. Progress and line count are displayed at the top.

---

## To do

- **Unit Tests**

---

## 📄 License

MIT License – Feel free to use and adapt this project for your own dataset collection efforts!