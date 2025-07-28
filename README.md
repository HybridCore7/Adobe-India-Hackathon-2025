# PDF Intelligence Toolkit — Adobe Hackathon 2025

Challenge Theme: Connecting the Dots Through Docs  
Hosted by: Adobe India | Hackathon 2025

## Project Summary

This project aims to redefine how we interact with PDFs — transforming static documents into smart, structured data that machines can easily interpret. Our system performs high-precision outline extraction and persona-aware content summarization from raw PDF files — all packaged in a fast, offline Docker container.

This repository contains solutions to:

- Round 1A — Structural Outline Extraction  
- Round 1B — Persona-Driven Document Intelligence

## Problem Overview

In the digital world, documents are everywhere — but understanding their structure and extracting insights at scale is still a challenge. Our goal is to:

- Extract meaningful structure (titles, H1-H3 headings) from raw PDFs
- Output clean, navigable JSON summaries
- Support future downstream tasks like semantic search or personalized recommendations

## Features

### Round 1A — PDF Outline Extractor

- Input: A PDF document (up to 50 pages)
- Output: JSON containing:
  - Document title
  - Headings (H1, H2, H3) with page numbers and hierarchy
- Executes offline in under 10 seconds on AMD64 CPUs
- No internet dependency, model size within 200MB

### Round 1B — Contextual Relevance Summarizer

- Input:
  - 3–10 related documents
  - Persona definition
  - Job-to-be-done prompt
- Output: JSON with metadata and ranked sections/subsections
- Execution time under 60 seconds, CPU-only
- Generalizable across domains such as research, finance, and education

## Tech Stack

- Python
- PyMuPDF / pdfminer.six for PDF parsing
- scikit-learn, transformers for lightweight ML models
- Docker for containerization
- nltk, regex, spacy for preprocessing

## How to Build and Run

### Build the Docker Image

```bash
docker build --platform linux/amd64 -t pdf-intelligence:alpha .

DOCKER RUN COMMAND :

docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-intelligence:alpha

REPOISTARY STRUCTURE:

├── app.py                   # Main PDF processor
├── Dockerfile               # Docker setup
├── requirements.txt         # Python dependencies
├── input/                   # Input PDFs (e.g., sample.pdf)
├── output/                  # Output JSONs (e.g., sample.json)
├── docker/                  # Additional Docker files/utilities
├── sample_scored.json       # Output sample for validation
└── README.md                # Project documentation

### Round 1A — PDF Outline Extractor

- Input: A PDF document (up to 50 pages)
- Output: JSON containing:
  - Document title
  - Headings (H1, H2, H3) with page numbers and hierarchy
- Executes offline in under 10 seconds on AMD64 CPUs
- No internet dependency, model size within 200MB

### Round 1B — Contextual Relevance Summarizer

- Input:
  - 3–10 related documents
  - Persona definition
  - Job-to-be-done prompt
- Output: JSON with metadata and ranked sections/subsections
- Execution time under 60 seconds, CPU-only
- Generalizable across domains such as research, finance, and education





