#!/usr/bin/env python3
"""
Meeting Summarizer Web Interface using Streamlit

This application allows users to:
  - Type a custom meeting name
  - Upload a transcript file (in TXT format) or an audio file
  - Generates a summarized meeting output using OpenAI's GPT-4o-mini

Requirements:
  - Python 3.x
  - Packages: streamlit, python-dotenv, openai
  - A .env file with the variable OPENAI_API_KEY (should start with "sk-proj-")
"""

import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------------------------------------------------------
# Configuration and Initialization
# -----------------------------------------------------------------------------

load_dotenv(override=True)

API_KEY = os.getenv("OPENAI_API_KEY")

def check_api_key(api_key: str) -> bool:
    if not api_key:
        st.error("Error: No API key found. Please check your .env file.")
        return False
    elif not api_key.startswith("sk-proj-"):
        st.error("Error: API key does not start with 'sk-proj-'. Please check your key.")
        return False
    elif api_key.strip() != api_key:
        st.error("Error: API key has leading or trailing whitespace.")
        return False
    else:
        st.success("API key found and valid.")
        return True

if not check_api_key(API_KEY):
    st.stop()

# Initialize the OpenAI client
openai = OpenAI()

AUDIO_MODEL = "whisper-1"
GPT4O_MODEL = "gpt-4o-mini"

# -----------------------------------------------------------------------------
# Whisper Transcription (Audio -> Text)
# -----------------------------------------------------------------------------

def transcribe_audio_file_on_disk(filename: str) -> str:
    """
    Transcribe the given audio file using OpenAI Whisper,
    returning the raw text from the transcription.
    """
    with open(filename, "rb") as audio_file:
        transcription = openai.audio.transcriptions.create(
            model=AUDIO_MODEL,
            file=audio_file,
            response_format="text"
        )
    return transcription

# -----------------------------------------------------------------------------
# Summarization with GPT-4o-mini (Text -> Summary)
# -----------------------------------------------------------------------------

def generate_meeting_summary(transcript: str, meeting_name: str) -> str:
    """
    Generates a meeting summary from a plain text transcript using GPT-4o-mini.
    
    Args:
        transcript (str): The plain text transcript of the meeting.
        meeting_name (str): The user-provided meeting name.
        
    Returns:
        str: The generated meeting summary in Markdown format.
    """
    # Fallback if meeting_name is empty
    if not meeting_name.strip():
        meeting_name = "meeting"

    system_prompt = (
        "You are an assistant that produces minutes of meetings from transcripts, "
        "with summary, key discussion points, takeaways, and action items with owners, in markdown."
    )
    user_prompt = (
        f"Below is an extract transcript of the {meeting_name}. "
        "Please write minutes in markdown, including a summary with attendees, location, and date; "
        "discussion points; takeaways; and action items with owners.\n"
        f"{transcript}"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    response = openai.chat.completions.create(
        model=GPT4O_MODEL,
        messages=messages
    )
    summary = response.choices[0].message.content
    return summary

# -----------------------------------------------------------------------------
# Streamlit Interface
# -----------------------------------------------------------------------------

st.title("Meeting Summarizer")

# Text input for meeting name
meeting_name = st.text_input(
    label="Enter the meeting name",
    value="",  # default empty
    placeholder="E.g. 'Denver city council meeting' or 'Weekly Marketing Sync'"
)

st.write("Upload your meeting transcript in text form **or** upload an audio file. Both use GPT-4o-mini summarization.")

upload_type = st.radio(
    "Select your upload type:",
    ("Text Transcript", "Audio File")
)

if upload_type == "Text Transcript":
    uploaded_text_file = st.file_uploader("Upload a TXT transcript", type=["txt"])
    if uploaded_text_file is not None:
        transcript_text = uploaded_text_file.read().decode("utf-8")
        st.write("Transcript loaded successfully.")

        with st.spinner("Generating meeting summary..."):
            summary_output = generate_meeting_summary(transcript_text, meeting_name)

        st.success("Meeting summary generated!")
        st.markdown(summary_output)

elif upload_type == "Audio File":
    uploaded_audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "ogg"])
    if uploaded_audio_file is not None:
        st.write("Audio file uploaded successfully.")
        filename, file_ext = os.path.splitext(uploaded_audio_file.name)
        if not file_ext:
            file_ext = ".mp3"  # default if none

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(uploaded_audio_file.read())
            temp_filename = tmp_file.name

        with st.spinner("Transcribing audio with Whisper..."):
            transcription_text = transcribe_audio_file_on_disk(temp_filename)

        st.write("Transcription complete!")
        with st.spinner("Generating meeting summary..."):
            summary_output = generate_meeting_summary(transcription_text, meeting_name)

        st.success("Meeting summary generated!")
        st.markdown(summary_output)