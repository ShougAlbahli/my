# Research Paper Summarizer

This simple Flask application allows users to upload a PDF, DOCX, or TXT file containing a research paper. The server extracts the text and uses GPT‑4 to summarize four key parts of the paper:

1. Problem Statement
2. Methodology
3. Results
4. Conclusion

The resulting summary is shown in the browser and can be downloaded as a PDF. The app does not store files permanently.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your `OPENAI_API_KEY` environment variable.
3. Run the server:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000` in your browser and upload a file.
