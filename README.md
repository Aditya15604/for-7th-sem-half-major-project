# 🛡️ Cyber Triage Tool

A comprehensive cyber security incident response and forensics tool with **intelligent automated analysis** and **modern web interface**.

## ✨ Features

### Core Analysis
- **Quick Scan Mode**: Rapid triage with file hashing, entropy analysis, PE inspection, and YARA detection
- **Full Analysis Mode**: Comprehensive system analysis (expandable for memory, registry, EVTX)
- **Real-time Progress Tracking**: Live scan status updates via WebSocket
- **AI-Powered Insights**: Intelligent threat assessment and recommendations

### Detection Capabilities
- **Entropy Analysis**: Detect encrypted, packed, or obfuscated files
- **PE File Analysis**: Windows executable metadata extraction (imphash, timestamps, sections)
- **YARA Malware Detection**: Pattern matching with included malware signatures
- **Threat Intelligence**: Mock threat intel API (ready for VirusTotal/OTX integration)

### Modern Web Interface
- **Interactive Dashboard**: Real-time statistics and case management
- **Beautiful UI**: Gradient designs, smooth animations, responsive layout
- **Detailed Reports**: Charts, tables, and AI-generated insights
- **One-Click Scanning**: Initiate scans directly from the web interface

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Windows PowerShell (for automation scripts)

### Installation

1. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```powershell
   python .\main.py --help
   ```

## 📖 Usage

### Command Line Interface

**Quick Scan:**
```powershell
python .\main.py --quick-scan C:\Users\Example\Documents --output-dir data\cases
```

**Full Analysis:**
```powershell
python .\main.py --full-analysis --target C:\Suspicious\Path
```

**Start Web Interface:**
```powershell
python .\main.py --web-interface
```

Then open your browser to: `http://127.0.0.1:8000`

### Web Interface

1. **Start the server:**
   ```powershell
   python .\main.py --web-interface
   ```

2. **Access the dashboard:**
   - Navigate to `http://127.0.0.1:8000`
   - View statistics and recent cases
   - Click "New Scan" to analyze a directory
   - View detailed reports with AI insights

### One-Click Investigation (PowerShell)
```powershell
.\scripts\one_click_investigation.ps1 -Target "C:\Path\To\Analyze"
```

## 📊 Reports

Reports are automatically generated in `data/cases/CASE-<timestamp>/`:
- **report.json**: Structured data with all findings
- **report.html**: Standalone HTML report

### Report Contents
- File hashes (SHA256)
- Entropy scores
- PE file information
- YARA match results
- Threat flags (high_entropy, executable, yara_match)
- AI-powered risk assessment

## 🎯 YARA Rules

Sample YARA rules are included in `config/yara/`:
- **malware_indicators.yar**: Common malware patterns
- **crypto_miners.yar**: Cryptocurrency miner detection

Add your own `.yar` files to this directory for custom detection.

## 🔧 Configuration

Edit `config/default.yaml` to customize:
- Maximum file size for scanning
- YARA rules directory
- Web interface host/port
- Logging levels

## 🏗️ Project Structure

```
cyber-triage-tool/
├── config/              # Configuration files and YARA rules
├── data/cases/          # Generated investigation reports
├── scripts/             # Automation scripts
├── src/
│   ├── analyzers/       # File analysis modules
│   ├── collectors/      # Data collection modules
│   ├── reporting/       # Report generation
│   ├── utils/           # Utility functions
│   ├── web/             # Flask web application
│   └── triage_engine.py # Core orchestration
├── tests/               # Test suite
├── main.py              # CLI entry point
└── requirements.txt     # Python dependencies
```

## 🧪 Testing

Run tests with pytest:
```powershell
pytest tests/
```

## 🔐 Security Notes

- The web interface binds to localhost by default
- Change the SECRET_KEY in production
- Add authentication for production deployments
- Review all YARA rules before use

## 🚧 Roadmap

- [ ] Memory forensics with Volatility3
- [ ] Windows Registry analysis
- [ ] Event log (EVTX) parsing
- [ ] Network traffic analysis (PCAP)
- [ ] Real-time monitoring mode
- [ ] VirusTotal API integration
- [ ] Export to STIX/MISP formats
- [ ] Multi-threaded scanning
- [ ] Database backend for case management

## 📝 License

This project is for educational and professional use in cybersecurity incident response.

## 🤝 Contributing

Contributions welcome! Please ensure:
- Code follows existing style
- Tests pass
- Documentation is updated

## 📧 Support

For issues or questions, please open a GitHub issue.

---

**Version**: 0.1.0  
**Status**: Active Development  
**Last Updated**: October 2025

