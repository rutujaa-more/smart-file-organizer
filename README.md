# 📁 Smart File Organizer

A Python-based web application that automatically categorizes uploaded files and organizes them into structured folders based on their file type.

🌐 **Live Demo:** https://smart-file-organizer-e9x434wnj9ybfpjr64ltfj.streamlit.app/

💻 **GitHub:** https://github.com/rutujaa-more/smart-file-organizer

## ✨ Features

* 📂 Automatically categorizes files by extension
* 🖼️ Supports images, videos, audio, documents, spreadsheets, presentations, archives, code, and executables
* 🔍 Provides a file analysis preview before organization
* 📊 Displays a summary of categorized files
* 🛡️ Prevents duplicate filenames from being overwritten
* 📦 Generates an organized ZIP archive
* 🌐 Accessible through a web-based Streamlit interface
* ⚡ Simple drag-and-drop file uploading

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Pathlib**
* **Zipfile**
* **Collections**
* **Git & GitHub**

## ⚙️ How It Works

```text
Upload Files
     ↓
Identify File Extensions
     ↓
Classify Files
     ↓
Create Category Structure
     ↓
Handle Duplicate Names
     ↓
Generate Organized ZIP
     ↓
Download Files
```

## 📁 Supported Categories

| Category          | Examples                  |
| ----------------- | ------------------------- |
| 🖼️ Images        | JPG, PNG, GIF, SVG, WEBP  |
| 🎬 Videos         | MP4, MKV, AVI, MOV        |
| 🎵 Audio          | MP3, WAV, FLAC, AAC       |
| 📄 Documents      | PDF, DOCX, TXT            |
| 📊 Spreadsheets   | XLSX, CSV, ODS            |
| 📽️ Presentations | PPTX, PPT, ODP            |
| 📦 Archives       | ZIP, RAR, 7Z, TAR         |
| 💻 Code           | PY, JS, JAVA, C, CPP, SQL |
| ⚙️ Executables    | EXE, MSI, APK, DMG        |
| 📁 Others         | Unsupported file types    |

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/rutujaa-more/smart-file-organizer.git
```

### 2. Open the project directory

```bash
cd smart-file-organizer
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will open locally at:

```text
http://localhost:8501
```

## 🔐 File Safety

The web application does not modify the original files on the user's computer. Uploaded files are processed by the application and returned as a newly generated ZIP archive.

## 📌 Future Improvements

* 🤖 Content-based file classification
* 📅 Automatic organization by date
* 🏷️ Custom user-defined categories
* 📈 File statistics and analytics
* 🔎 Duplicate-content detection
* 🧠 AI-powered file categorization
* 🖥️ Desktop version with direct folder organization

## 👩‍💻 Author

**Rutuja More**

Computer Science & Engineering Student

Built as a Python automation and web development project.
