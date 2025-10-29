# 🚀 Quick Start Guide

Get up and running with Cyber Triage Tool in 5 minutes!

## Step 1: Setup Environment

```powershell
# Clone or navigate to the project directory
cd "d:\BE Major Project All\my choice\cyber-triage-tool"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run Your First Scan

### Option A: Web Interface (Recommended)

```powershell
# Start the web server
python .\main.py --web-interface
```

Then:
1. Open browser to `http://127.0.0.1:8000`
2. Click "New Scan"
3. Enter a directory path (e.g., `C:\Users\YourName\Documents`)
4. Click "Start Scan"
5. View the generated report with AI insights!

### Option B: Command Line

```powershell
# Scan a directory
python .\main.py --quick-scan "C:\Users\YourName\Documents"

# View the report
# Reports are saved in data\cases\CASE-<timestamp>\
```

## Step 3: Explore Features

### View Dashboard Statistics
- Navigate to `http://127.0.0.1:8000`
- See total cases, files analyzed, threats detected

### Analyze Reports
- Click on any case to view detailed report
- See entropy analysis, PE file info, YARA matches
- Get AI-powered threat assessments

### Run Advanced Scans
```powershell
# Full analysis mode
python .\main.py --full-analysis --target "C:\Suspicious\Path"

# With verbose logging
python .\main.py --quick-scan "C:\Path" --verbose
```

## Common Use Cases

### 1. Scan Downloads Folder
```powershell
python .\main.py --quick-scan "$env:USERPROFILE\Downloads"
```

### 2. Investigate Suspicious Files
```powershell
python .\main.py --quick-scan "C:\Temp\SuspiciousFiles" --verbose
```

### 3. Automated Scanning
```powershell
.\scripts\one_click_investigation.ps1 -Target "C:\Path\To\Scan"
```

## Understanding Results

### Threat Indicators

- **High Entropy**: Files with entropy ≥ 7.5 (possible encryption/packing)
- **Executables**: PE files (.exe, .dll, .sys)
- **YARA Matches**: Files matching malware signatures

### Risk Levels

- **Low**: < 30% suspicious files
- **Medium**: 30-50% suspicious files
- **High**: > 50% suspicious files or YARA matches

## Troubleshooting

### Issue: Module not found
```powershell
# Ensure virtual environment is activated
.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port already in use
```powershell
# Use a different port
python .\main.py --web-interface --config config/default.yaml
# Then edit config/default.yaml to change port
```

### Issue: YARA not working
```powershell
# Install YARA Python bindings
pip install yara-python
```

## Next Steps

- 📖 Read the full [README.md](README.md)
- 🎯 Add custom YARA rules to `config/yara/`
- ⚙️ Customize settings in `config/default.yaml`
- 🧪 Run tests: `pytest tests/`

## Tips & Tricks

1. **Scan regularly**: Set up scheduled scans for critical directories
2. **Review YARA matches**: Always investigate files with YARA detections
3. **Check high entropy**: High entropy doesn't always mean malware, but investigate compressed/encrypted files
4. **Export reports**: Use the HTML reports for documentation
5. **Monitor trends**: Watch for increasing threat indicators over time

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review sample YARA rules in `config/yara/`
- Examine example reports in `data/cases/`

---

**Happy Triaging! 🛡️**
