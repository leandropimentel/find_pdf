from flask import Flask, request, render_template
from markupsafe import Markup
import fitz  # PyMuPDF
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

# Certifique-se de que a pasta de upload existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def search_text_in_pdf(pdf_path, search_term):
    doc = fitz.open(pdf_path)
    results = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if search_term.lower() in text.lower():
            # Use case-insensitive replacement
            highlighted_text = text.replace(search_term, f"<mark>{search_term}</mark>")
            results.append((page_num + 1, Markup(highlighted_text)))
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    pdf_file = request.files['pdf_file']
    if not pdf_file or not search_term:
        return "Please provide a PDF file and a search term", 400
    
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_path)

    results = search_text_in_pdf(pdf_path, search_term)
    return render_template('results.html', results=results, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
