# Research Paper Summarizer

This simple Flask application lets you upload a PDF, DOCX, or TXT file containing a research paper. It uses OpenAI's GPT-4 model to summarize the paper in plain English covering the problem statement, methodology, results, and conclusion. The summary is offered as a PDF download.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key in the environment:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```
3. Run the application:
   ```bash
   python app.py
   ```

Open your browser to `http://localhost:5000` and upload a research paper to get a summary.
