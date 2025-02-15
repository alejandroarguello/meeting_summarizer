#!/usr/bin/env python3
"""
Meeting Summarizer Web Interface using Streamlit

This application allows users to upload a transcript file (in TXT format) and generates 
a summarized meeting output using OpenAI's API.

Requirements:
  - Python 3.x
  - Packages: streamlit, python-dotenv, openai
  - A .env file in the project root with the variable OPENAI_API_KEY (should start with "sk-proj-")
"""

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------------------------------------------------------
# Configuration and Initialization
# -----------------------------------------------------------------------------

# Load environment variables from the .env file
load_dotenv(override=True)
API_KEY = os.getenv('OPENAI_API_KEY')

def check_api_key(api_key: str) -> bool:
    """
    Validates the API key.
    """
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

# -----------------------------------------------------------------------------
# Meeting Summary Generator Function
# -----------------------------------------------------------------------------

def generate_meeting_summary_from_text(transcript: str) -> str:
    """
    Generates meeting summary from a meeting transcript text.
    
    Parameters:
        transcript (str): The meeting transcript content.
    
    Returns:
        str: The generated meeting summary in Markdown format.
    """
    system_prompt = (
        "You are an expert meeting summary generator. You will be provided with a transcript from a Microsoft Teams meeting, "
        "which includes timestamps and speaker names. Your task is to analyze the transcript, extract the key discussion points, "
        "decisions made, and action items, and then produce a concise, well-organized summary. Format your output with clear headings "
        "such as 'Key Points', 'Decisions', and 'Action Items'. Ensure that your summary captures the context and important contributions."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": transcript},
    ]
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    summary = response.choices[0].message.content
    return summary

# -----------------------------------------------------------------------------
# Streamlit User Interface
# -----------------------------------------------------------------------------

st.title("Meeting Summarizer")
st.write("Upload your meeting transcript file (TXT format) to generate summarized meeting information.")

uploaded_file = st.file_uploader("Drag and drop your transcript file here", type=["txt"])

if uploaded_file is not None:
    # Read and decode the transcript file
    transcript_text = uploaded_file.read().decode("utf-8")
    st.write("Transcript loaded successfully. Generating meeting summary...")
    
    with st.spinner("Generating meeting summary..."):
        summary_output = generate_meeting_summary_from_text(transcript_text)
    
    st.success("Meeting summary generated!")
    st.markdown(summary_output)