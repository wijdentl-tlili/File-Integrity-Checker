# 🔐 File Integrity Checker (Python)

A lightweight **File Integrity Monitoring (FIM)** tool inspired by security solutions like Tripwire and AIDE.  
It detects **file modifications, deletions, and new file creation** using SHA-256 hashing.

---

## 🚀 Features

- 🔍 Recursive directory scanning
- 🔐 SHA-256 file integrity hashing
- 📊 Baseline creation & comparison
- 🧾 Detects:
  - Modified files
  - Deleted files
  - New files
- 🎨 Colored CLI output (SOC-style)
- 💻 Interactive CLI mode (Metasploit-like experience)
- 🛠 Manual baseline update option

---

## 🏗 Project Structure
cli_integrity_checker.py → Interactive CLI tool
integrity_checker.py → One-time integrity scan tool
baseline.json → Stored file fingerprints
requirements.txt → Dependencies

---

## ⚙️ Installation

### 1. Clone repository

```bash```
git clone https://github.com/your-username/file-integrity-checker.git
cd file-integrity-checker

### 2. Create virtual environment (recommended)

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

### 3. Install dependencies
pip install -r requirements.txt

## ▶️ Usage
### 🧪 Option 1: Interactive CLI (Recommended)
python cli_integrity_checker.py
Available commands:
check <directory>   → Scan and compare integrity
update              → Update baseline
help                → Show commands
exit                → Quit
### 🧪 Option 2: One-time scan mode
python integrity_checker.py

## 📊 Example Output
========== RESULTS ==========

[MODIFIED] C:\Cyber Project\File Integrity Checker\path_to_test\test.txt
[NEW] C:\Cyber Project\File Integrity Checker\path_to_test\two.txt

========== SUMMARY ==========
Modified files : 1
Deleted files  : 0
New files      : 1

## 🧠 How It Works
1. Files are scanned recursively
2. Each file is hashed using SHA-256
3. A baseline is stored in baseline.json
4. Future scans compare hashes:
    * Same hash → OK
    * Different hash → MODIFIED
    * Missing → DELETED
    * New file → NEW