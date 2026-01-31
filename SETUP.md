# Setup Guide: Quran Data Collection Script

## Prerequisites

- **Python 3.11+** (required)
- **pip** (Python package installer)
- **Git** (optional, for version control)

## Step 1: Create Virtual Environment (Mandatory)

A virtual environment isolates project dependencies from your system Python.

### Windows (PowerShell)

```powershell
# Navigate to project directory
cd "d:\Work\Quran Project\Tazkiyah"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Verify activation (should show venv path)
Get-Command python | Select-Object -ExpandProperty Source
```

### Windows (Command Prompt)

```cmd
cd "d:\Work\Quran Project\Tazkiyah"
python -m venv venv
venv\Scripts\activate.bat
```

### Linux / macOS

```bash
cd /path/to/Tazkiyah
python3 -m venv venv
source venv/bin/activate
```

## Step 2: Install Dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 3: Verify Installation

```bash
# Check installed packages
pip list

# Verify script can run
python collect_quran.py --help
```

## Step 4: Deactivate When Done

```bash
deactivate
```

## Troubleshooting

### PowerShell Execution Policy Error

If you see "running scripts is disabled on this system":

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python Not Found

Ensure Python 3.11+ is installed and added to PATH:

```powershell
python --version
```

### Permission Errors

On Linux/macOS, you may need to use `python3` and `pip3` instead of `python` and `pip`.

## Project Structure

After setup, your project should look like:

```
Tazkiyah/
├── venv/                     # Virtual environment (do not commit)
├── SETUP.md                  # This file
├── README.md                 # Usage guide
├── requirements.txt          # Dependencies
├── config.example.json       # Configuration template
├── collect_quran.py          # Main CLI entry point
├── quran_api.py              # API client module
├── collector.py              # Data collection logic
├── tafsir_fetcher.py         # Parallel tafsir fetching
├── validate_data.py          # Validation utility
└── convert_to_json.py        # JSONL → JSON converter
```

## Quick Start

```bash
# Activate venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/macOS

# List available translations and tafsirs
python collect_quran.py --list-resources

# Collect first 3 surahs (quick test)
python collect_quran.py --surah-range 1 3 --translations 131,85 --output test.jsonl

# Collect all surahs with tafsir
python collect_quran.py --all --translations 131,85 --tafsirs 169 --output quran_complete.jsonl
```
