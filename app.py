from flask import Flask, render_template, request, redirect, url_for, session
from transformers import pipeline, BartTokenizer
from PIL import Image
import pytesseract
import re
import os
import uuid

# TESSERACT CONFIG
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESSERACT_DIR = os.path.join(BASE_DIR, 'portable_tesseract_ocr')

tesseract_cmd_path = os.path.join(TESSERACT_DIR, 'tesseract.exe')
tessdata_path = os.path.join(TESSERACT_DIR, 'tessdata')

if os.path.exists(tesseract_cmd_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
    os.environ["TESSDATA_PREFIX"] = tessdata_path
    print(f"Using local Tesseract at: {tesseract_cmd_path}")
else:
    print(f"WARNING: Local Tesseract not found at {tesseract_cmd_path}. Please install or check path.")

# FLASK SETUP
app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# LOAD MODELS
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ROUTES
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Get uploaded file
        file = request.files.get("image")
        if not file or file.filename == "":
            return "No file selected", 400

        # Save with unique filename
        filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Load image
        image = Image.open(file_path)

        # OCR
        try:
            ocr_text = pytesseract.image_to_string(image)
        except Exception as e:
            return f"OCR Failed: {e}", 500

        # Clean text
        cleaned_text = re.sub(r"[\n\f]+", " ", ocr_text).strip()

        # SUMMARIZATION
        if cleaned_text:
            # Count tokens
            tokens = tokenizer.encode(cleaned_text, return_tensors="pt")
            num_tokens = tokens.shape[1]

            summary = summarizer(
                cleaned_text,
                max_length=min(1024, num_tokens),
                min_length=20,
                do_sample=False
            )[0]["summary_text"]
        else:
            summary = "No text detected in the image."

        # Store results
        session["image_path"] = file_path
        session["ocr_text"] = ocr_text
        session["summary"] = summary

        return redirect(url_for("index"))

    # GET request -> load results
    return render_template(
        "index.html",
        image_path=session.pop("image_path", None),
        ocr_text=session.pop("ocr_text", None),
        summary=session.pop("summary", None)
    )

# RUN APP
if __name__ == "__main__":
    print("\n" + "="*60)
    print("OCR Summarizer")
    print("="*60 + "\n")
    
    print("Server running at: http://localhost:5000\n")
    
    app.run(debug=True, port=5000)