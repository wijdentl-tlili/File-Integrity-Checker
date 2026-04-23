# File Integrity Checker 🔐

File Integrity Checker (FIM) monitors a directory and alerts you when files are **modified**, **deleted**, or **created** — useful for detecting tampering, auditing changes, or maintaining system hygiene.

## 📊 Example Output
```
========== RESULTS ==========

[MODIFIED] \path_to_test\test.txt
[NEW] \path_to_test\two.txt

========== SUMMARY ==========
Modified files : 1
Deleted files  : 0
New files      : 1
```

---

## Features

- **SHA-256 hashing** — cryptographically strong file fingerprinting
- **Recursive scanning** — monitors entire directory trees
- **Baseline system** — stores snapshots in `baseline.json` for future comparison
- **Change detection** — catches modified, deleted, and newly created files
- **Colored CLI output** — instant visual distinction between change types
- **Interactive mode** — run continuous checks without restarting the tool
- **Manual baseline updates** — refresh the baseline whenever you're ready

---

## Project Structure

```
file-integrity-checker/
├── cli_integrity_checker.py   # Interactive CLI mode (recommended)
├── integrity_checker.py       # One-time scan mode
├── baseline.json              # Stored file hashes (auto-generated)
└── requirements.txt           # Dependencies
```

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/wijdentl-tlili/File-Integrity-Checker.git
cd file-integrity-checker
```

**2. Create a virtual environment** *(recommended)*
```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Usage

### Option 1 — Interactive CLI *(recommended)*

```bash
python cli_integrity_checker.py
```

| Command              | Description                        |
|----------------------|------------------------------------|
| `check <directory>`  | Scan and compare against baseline  |
| `update`             | Update the baseline with new hashes|
| `help`               | Show available commands            |
| `exit`               | Quit the tool                      |

### Option 2 — One-time scan

```bash
python integrity_checker.py
```

Runs a single scan against the existing baseline and exits.

---

## How It Works

```
Directory scan  →  SHA-256 hash each file  →  Compare with baseline.json
                                                       │
                              ┌────────────────────────┤
                              ▼                        ▼
                        Hash matches?              Missing?
                           → OK                   → DELETED
                        Hash differs?            Not in baseline?
                           → MODIFIED               → NEW
```

On first run, a baseline is created. Every subsequent scan compares live hashes against that baseline — any deviation is flagged immediately.

---

## When to Use This

- Monitoring sensitive config files or scripts for unexpected changes
- Auditing file activity in shared or development environments
- Learning about file integrity monitoring concepts
- Lightweight alternative to enterprise FIM tools for personal projects

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## Author

**Wijden Tlili** — [GitHub](https://github.com/wijdentl-tlili)
