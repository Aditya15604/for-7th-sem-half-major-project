# 🏗️ Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│  Web Browser                    │  Command Line Interface       │
│  - Dashboard                    │  - Quick Scan                 │
│  - Scan Page                    │  - Full Analysis              │
│  - Report Viewer                │  - Investigation Mode         │
└─────────────────┬───────────────┴───────────────┬───────────────┘
                  │                               │
                  ▼                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  Flask Web App (app.py)         │  Main CLI (main.py)           │
│  - Routes                       │  - Argument Parsing           │
│  - API Endpoints                │  - Mode Selection             │
│  - SocketIO Events              │  - Logging Setup              │
└─────────────────┬───────────────┴───────────────┬───────────────┘
                  │                               │
                  └───────────────┬───────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TRIAGE ENGINE                              │
│                   (triage_engine.py)                            │
├─────────────────────────────────────────────────────────────────┤
│  - Orchestrates analysis workflow                              │
│  - Manages case directories                                    │
│  - Coordinates analyzers and collectors                        │
│  - Generates reports                                           │
└─────────────────┬───────────────────────────────┬───────────────┘
                  │                               │
        ┌─────────┴─────────┐         ┌──────────┴──────────┐
        ▼                   ▼         ▼                     ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  COLLECTORS  │  │  ANALYZERS   │  │   REPORTING  │  │   UTILITIES  │
├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤
│ File         │  │ Entropy      │  │ JSON Writer  │  │ Logger       │
│ Collector    │  │ Analyzer     │  │ HTML Writer  │  │ Config       │
│              │  │              │  │ Case Manager │  │ Hash         │
│ - Recursive  │  │ PE Analyzer  │  │              │  │ Computer     │
│   Traversal  │  │              │  │              │  │              │
│ - Size       │  │ YARA Scanner │  │              │  │              │
│   Filtering  │  │              │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
        │                   │                │                │
        └───────────────────┴────────────────┴────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│  File System                    │  Configuration                │
│  - data/cases/                  │  - config/default.yaml        │
│  - data/evidence/               │  - config/yara/*.yar          │
│  - logs/                        │                               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

#### Web Interface
```
┌─────────────────────────────────────┐
│         Web Application             │
├─────────────────────────────────────┤
│  Templates/                         │
│  ├── navbar.html (Navigation)       │
│  ├── index.html (Dashboard)         │
│  ├── scan.html (Scan Page)          │
│  └── report_new.html (Reports)      │
│                                     │
│  Static/                            │
│  ├── css/style.css                  │
│  └── js/dashboard.js                │
└─────────────────────────────────────┘
```

#### CLI Interface
```
main.py
├── --quick-scan <path>
├── --full-analysis --target <path>
├── --investigate --case-id <id>
├── --web-interface
└── --help
```

### 2. Application Layer

#### Flask Routes
```python
/                       → Dashboard (index.html)
/scan                   → Scan initiation page
/report/<case_id>       → Report viewer

# API Endpoints
/api/cases              → List all cases
/api/report/<case_id>   → Get case data
/api/stats              → Dashboard statistics
/api/scan               → Start new scan (POST)
/api/scan/<id>/status   → Check scan progress
/api/threat-intel/<hash>→ Threat intelligence
```

### 3. Core Engine

#### Triage Engine Workflow
```
┌──────────────────────────────────────────────────────────┐
│                    TRIAGE ENGINE                         │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │   1. Initialize Case          │
            │   - Create case directory     │
            │   - Generate case ID          │
            └───────────────┬───────────────┘
                            ▼
            ┌───────────────────────────────┐
            │   2. Collect Files            │
            │   - Recursive traversal       │
            │   - Apply size filters        │
            │   - Build file list           │
            └───────────────┬───────────────┘
                            ▼
            ┌───────────────────────────────┐
            │   3. Analyze Each File        │
            │   ├─ Compute hashes           │
            │   ├─ Calculate entropy        │
            │   ├─ Check PE structure       │
            │   └─ Run YARA rules           │
            └───────────────┬───────────────┘
                            ▼
            ┌───────────────────────────────┐
            │   4. Generate Flags           │
            │   - high_entropy (≥7.5)       │
            │   - executable (PE files)     │
            │   - yara_match (detections)   │
            └───────────────┬───────────────┘
                            ▼
            ┌───────────────────────────────┐
            │   5. Create Reports           │
            │   - JSON (structured data)    │
            │   - HTML (visual report)      │
            └───────────────────────────────┘
```

### 4. Analyzer Components

#### Entropy Analyzer
```
Input: File path
  │
  ▼
Read file in chunks (1MB)
  │
  ▼
Count byte frequencies
  │
  ▼
Calculate Shannon entropy: H = -Σ(p(x) * log2(p(x)))
  │
  ▼
Output: {"entropy": 7.5837}
```

#### PE Analyzer
```
Input: File path
  │
  ▼
Check file extension (.exe, .dll, .sys, .ocx)
  │
  ├─ Not PE extension → {"is_pe": false}
  │
  ▼
Parse PE structure (fast_load=True)
  │
  ▼
Extract metadata:
  ├─ Number of sections
  ├─ Import hash (imphash)
  └─ Compilation timestamp
  │
  ▼
Output: {"is_pe": true, "imphash": "...", ...}
```

#### YARA Scanner
```
Input: File path, Rules directory
  │
  ▼
Compile YARA rules from directory
  │
  ▼
Scan file against compiled rules
  │
  ▼
Collect matches
  │
  ▼
Output: ["Ransomware_Indicators", "Suspicious_PE"]
```

### 5. Data Flow

#### Scan Request Flow
```
User clicks "Start Scan"
        │
        ▼
POST /api/scan
        │
        ▼
Create scan_id and background thread
        │
        ▼
Return scan_id to client
        │
        ▼
Client polls /api/scan/<id>/status
        │
        ▼
Background thread:
  ├─ Initialize TriageEngine
  ├─ Run quick_scan()
  ├─ Update scan_progress
  └─ Set status to "completed"
        │
        ▼
Client receives completion
        │
        ▼
Redirect to /report/<case_id>
```

#### Report Generation Flow
```
Scan completes
        │
        ▼
Aggregate results
        │
        ▼
Create summary:
  ├─ case_id
  ├─ generated_at
  ├─ target
  └─ count
        │
        ▼
Write JSON report
        │
        ▼
Generate HTML report
        │
        ▼
Save to case directory
```

## Technology Stack

### Backend
```
Python 3.10+
├── Flask (Web framework)
├── Flask-SocketIO (Real-time communication)
├── PyYAML (Configuration)
├── yara-python (Malware detection)
├── pefile (PE analysis)
└── psutil (System info)
```

### Frontend
```
HTML5 + CSS3 + JavaScript
├── Bootstrap 5 (UI framework)
├── Bootstrap Icons (Icons)
├── Chart.js (Visualizations)
└── Fetch API (AJAX requests)
```

### Analysis Tools
```
Custom Implementations
├── Shannon Entropy Calculator
├── Hash Computer (SHA256, MD5, SHA1)
├── File Collector
└── Report Generator

External Libraries
├── YARA (Pattern matching)
└── pefile (PE parsing)
```

## Security Architecture

### Defense Layers
```
┌─────────────────────────────────────────┐
│  Layer 1: Network                       │
│  - Localhost binding (127.0.0.1)        │
│  - Configurable port                    │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  Layer 2: Application                   │
│  - Input validation                     │
│  - Error handling                       │
│  - Secret key management                │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  Layer 3: File System                   │
│  - File size limits                     │
│  - Symlink protection                   │
│  - Path validation                      │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  Layer 4: Analysis                      │
│  - Safe parsing (fast_load)             │
│  - Exception handling                   │
│  - Resource limits                      │
└─────────────────────────────────────────┘
```

## Deployment Architecture

### Development
```
Local Machine
├── Python Virtual Environment
├── Flask Development Server
├── File-based storage
└── Console logging
```

### Production (Recommended)
```
Server
├── WSGI Server (Gunicorn/uWSGI)
├── Reverse Proxy (Nginx)
├── SSL/TLS Certificates
├── Database (PostgreSQL/MySQL)
├── Authentication (OAuth/LDAP)
├── Log Aggregation (ELK Stack)
└── Monitoring (Prometheus/Grafana)
```

## Extensibility Points

### Adding New Analyzers
```python
# 1. Create analyzer in src/analyzers/
def analyze_file(path: Path) -> dict:
    # Your analysis logic
    return {"result": "..."}

# 2. Import in triage_engine.py
from .analyzers.new_analyzer import analyze_file as new_analyze

# 3. Add to analysis pipeline
record["new_analysis"] = new_analyze(fp)
```

### Adding New API Endpoints
```python
# In src/web/app.py
@app.route("/api/new-endpoint")
def new_endpoint():
    # Your logic
    return jsonify({"data": "..."})
```

### Adding New YARA Rules
```
# Create file in config/yara/
rule New_Detection {
    meta:
        description = "..."
    strings:
        $pattern = "..."
    condition:
        $pattern
}
```

## Performance Considerations

### Current Optimizations
- Streaming I/O (1MB chunks)
- Fast PE loading
- Lazy YARA compilation
- Background threading
- File size limits

### Scalability Limits
- Single-threaded file processing
- In-memory scan tracking
- File-based storage
- No result caching

### Future Optimizations
- Multi-process pool
- Redis for scan tracking
- Database for results
- Result caching
- Incremental scanning

---

**For implementation details, see source code in `src/` directory.**

