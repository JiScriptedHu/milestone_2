# OCR Summarizer

A Flask web application that extracts text from uploaded images using OCR (Optical Character Recognition) and generates a concise summary using a pre-trained Transformer model.

## Features

* **Image Upload**: Drag-and-drop or file selection for image uploads.
* **OCR Extraction**: Uses Tesseract OCR to convert images to text.
* **Text Summarization**: Uses the Facebook BART Large CNN model (via Hugging Face Transformers) to summarize extracted text.
* **Clean UI**: Minimalist, responsive design.

## Tech Stack

* **Backend**: Flask (Python)
* **OCR**: Tesseract (via `pytesseract` and `Pillow`)
* **AI/ML**: Hugging Face Transformers (`facebook/bart-large-cnn`) & PyTorch
* **Frontend**: HTML, CSS, JS

## How to Use

1. Allow script execution for the current process
```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```

2. Create the virtual environment
```bash
python -m venv venv
```

3. Activate the environment
```bash
.\venv\Scripts\activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Run the applicaton
```bash
python app.py
```

6. Open your browser and navigate to
```bash
http://localhost:5000
```

<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/96f9eb48-e2d1-40c0-970e-7bda31fc082b" />
