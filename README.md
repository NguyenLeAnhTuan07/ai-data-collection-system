# AI Data Acquisition System

## Introduction

In this article, I would like to share several programs designed to collect image data for AI training purposes.

This project provides an automated data acquisition system that supports the collection, processing, and organization of image datasets for artificial intelligence and machine learning applications. It is designed to help researchers and developers efficiently build high-quality datasets for training AI models.

The system may include functionalities such as:

- Web crawling and scraping
- Image downloading and filtering
- OCR-based text extraction
- Dataset preprocessing and organization

---

# Project Setup Guide

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-data-acquisition-system.git
cd ai-data-acquisition-system
```

---

## 2. Create and Activate Virtual Environment (venv)

It is highly recommended to use a virtual environment to isolate project dependencies.

### On Windows (Git Bash / CMD / PowerShell)

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Git Bash:

```bash
source venv/Scripts/activate
```

CMD:

```bash
venv\Scripts\activate
```

PowerShell:

```bash
venv\Scripts\Activate.ps1
```

If activated successfully, you will see `(venv)` at the beginning of your terminal line.

---

### On Linux / macOS

Create virtual environment:

```bash
python3 -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

---

## 3. Install Required Libraries

After activating the virtual environment, install all required dependencies using:

```bash
pip install -r requirements.txt
```

This command will automatically install all necessary Python libraries for the project.

---

## 4. Important: Read setup.txt Carefully

If the project directory contains a file named `setup.txt`, please read it carefully before running the program.

The `setup.txt` file may include:

- Additional configuration instructions
- External tool installation requirements (e.g., Tesseract OCR, Playwright browsers)
- Environment variable setup
- Special system dependencies

Make sure all instructions in `setup.txt` are completed to avoid runtime errors.

---

Thank you for reading and exploring this project.  
Wishing everyone a productive and wonderful day!

**Nguyen Le Anh Tuan**
