# app.py
import pdfplumber
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('punkt_tab')
import re
import os
import sys

# --- NLTK Data Download (for sentence and sumy Tokenizer) ---
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("NLTK 'punkt' data not found. Downloading...")
    nltk.download('punkt', quiet=True)

from nltk.tokenize import sent_tokenize

def extract_pdf_info(pdf_path, purpose_description):
    text_content = ""
    headings = []
    title = ""

    with pdfplumber.open(pdf_path) as pdf:
        # Extract title from the first page's first line
        first_page = pdf.pages[0]
        text_on_first_page = first_page.extract_text()
        if text_on_first_page:
            lines = text_on_first_page.strip().split('\n')
            if lines:
                title = lines[0].strip()

        # Extract all text content
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_content += page_text + "\n"

            # Extract potential headings based on font size and formatting
            for obj in page.extract_words(x_tolerance=2, y_tolerance=2, keep_blank_chars=False, use_text_flow=True):
                if 'fontname' in obj and 'size' in obj:
                    if obj['size'] > 12:  # Heuristic for headings
                        line = obj['text'].strip()
                        if line and re.match(r"^[A-Z][^.]*$", line) and len(line.split()) < 10:
                            if line not in headings:
                                headings.append(line)

    headings = list(dict.fromkeys(headings))  # Remove duplicates while preserving order

    # Generate summary using LSA
    parser = PlaintextParser.from_string(text_content, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, sentences_count=5)
    summary = " ".join([str(sentence) for sentence in summary_sentences])

    # Section relevance scoring using Sentence Transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')
    purpose_embedding = model.encode([purpose_description])

    section_scores = {}
    for heading in headings:
        heading_embedding = model.encode([heading])
        score = cosine_similarity(purpose_embedding, heading_embedding)[0][0]
        section_scores[heading] = round(score * 60, 2)  # Score scaled to max 60

    ranked_sections = sorted(section_scores.items(), key=lambda x: x[1], reverse=True)

    return {
        "title": title,
        "summary": summary,
        "headings": headings,
        "ranked_section_relevance": [
            {"section": section, "score_out_of_60": score}
            for section, score in ranked_sections
        ]
    }

# Main execution block
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <path_to_pdf>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]

    if not os.path.exists(pdf_file_path):
        print(f"Error: PDF file not found at {pdf_file_path}")
        sys.exit(1)

    try:
        print("\n--- PDF Extractor and Scorer ---")
        purpose = input("What is your purpose for extracting information from this PDF (e.g., job description keywords, research interest)?\n> ")
        if not purpose.strip():
            print("Purpose cannot be empty. Exiting.")
            sys.exit(1)

        extracted_data = extract_pdf_info(pdf_file_path, purpose)

        output_json_path = os.path.splitext(pdf_file_path)[0] + "_scored.json"
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)

        print(f"\n✅ Successfully extracted and scored information to {output_json_path}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
