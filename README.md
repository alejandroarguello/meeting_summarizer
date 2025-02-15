# Meeting Summarizer 📝

A Streamlit-based web application that generates concise summaries from meeting transcripts using OpenAI's GPT-4 model. Ideal for Microsoft Teams meeting transcripts with timestamps and speaker names.

## Features 🚀
- Upload TXT transcripts and generate summaries
- Key sections: **Key Points**, **Decisions**, **Action Items**
- Validates OpenAI API key format for security
- Clean, user-friendly interface

## Prerequisites ⚙️
- Python 3.x
- OpenAI API key (starts with `sk-proj-`)

## Installation 📦
1. Clone the repository:
   ```bash
   git clone https://github.com/alejandroarguello/meeting_summarizer.git
   cd meeting_summarizer

2. Install dependencies:
   ```
   pip install -r requirements.txt

3. Create a .env file in the root directory:
   ```bash
   OPENAI_API_KEY=sk-proj-your-key-here

## Usage ▶️
1. Run the app explicitly using the Python interpreter from your active conda environment:
   ```
   python -m streamlit run app.py

2. Upload a TXT transcript via the web interface.

3. View the generated summary in Markdown format.

## Example 🎯
Try the included 'sample_transcript.txt' to see a demo summary.

## Configuration 🔧

| File      | Purpose |
| ----------- | ----------- |
| app.py      | Main application logic       |
| .env   | Stores OpenAI API key        |
| requirements.txt   | Lists Python dependencies        |


## Troubleshooting ❌

❌ **"API key invalid"** &rarr; Ensure your key starts with 'sk-proj-' and has no whitespace.

❌ **File upload errors** &rarr; Verify the TXT file is properly formatted.

## Note 📌
This app is optimized for Microsoft Teams transcripts but works with any properly formatted TXT file containing speaker labels and timestamps.