import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
import openai
from PyPDF2 import PdfReader
import docx
from fpdf import FPDF

auth = os.getenv("OPENAI_API_KEY")
openai.api_key = auth

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app = Flask(__name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(file_path, ext):
    if ext == "pdf":
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == "docx":
        doc = docx.Document(file_path)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    return text


def summarize_text(text):
    prompt = (
        "Summarize the following research paper in plain English.\n"
        "Focus on four sections: (1) Problem Statement, (2) Methodology,"
        " (3) Results, and (4) Conclusion."
    )
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text[:6000]},  # limit tokens
    ]
    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    return response.choices[0].message.content.strip()


def create_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary.splitlines():
        pdf.multi_cell(0, 10, line)
    file_stream = BytesIO()
    pdf.output(file_stream)
    file_stream.seek(0)
    return file_stream


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[1].lower()
            tmp_path = os.path.join("/tmp", filename)
            file.save(tmp_path)
            text = extract_text(tmp_path, ext)
            summary = summarize_text(text)
            pdf_file = create_pdf(summary)
            return render_template("summary.html", summary=summary)
        return render_template("index.html", error="Unsupported file type")
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_pdf():
    summary = request.form.get("summary")
    if not summary:
        return "No summary found", 400
    pdf_file = create_pdf(summary)
    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="summary.pdf",
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(debug=True)
