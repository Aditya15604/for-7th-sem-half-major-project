# 🎯 Feature Documentation

## Intelligent Analysis Features

### 1. AI-Powered Threat Assessment

The tool automatically analyzes scan results and provides intelligent insights:

#### Risk Level Calculation
- **Low Risk**: < 30% suspicious files, no YARA matches
- **Medium Risk**: 30-50% suspicious files, or 10+ executables
- **High Risk**: > 50% suspicious files, or any YARA matches

#### Automated Recommendations
Based on findings, the system provides actionable recommendations:
- Quarantine instructions for YARA matches
- Investigation guidance for high-entropy files
- Security best practices
- Monitoring suggestions

### 2. Real-Time Scanning

#### Progress Tracking
- Live scan status updates
- Progress percentage display
- Estimated completion time
- Background processing with threading

#### WebSocket Integration
- Real-time communication between server and client
- Instant status updates without page refresh
- Responsive UI feedback

### 3. Advanced File Analysis

#### Entropy Analysis
**Purpose**: Detect encrypted, packed, or obfuscated files

**How it works**:
- Calculates Shannon entropy (0-8 scale)
- Flags files with entropy ≥ 7.5
- Identifies potential malware obfuscation

**Interpretation**:
- 0-3: Plain text, low compression
- 3-5: Moderate compression
- 5-7: High compression
- 7-8: Encryption or packing (suspicious)

#### PE File Analysis
**Purpose**: Extract metadata from Windows executables

**Extracted Information**:
- Import hash (imphash) for malware family identification
- Compilation timestamp
- Number of sections
- PE validity check

**Use Cases**:
- Identify malware variants by imphash
- Detect timestamp anomalies
- Verify executable authenticity

#### YARA Detection
**Purpose**: Pattern-based malware detection

**Included Rules**:
1. **malware_indicators.yar**
   - Suspicious PE characteristics
   - Ransomware indicators
   - PowerShell obfuscation
   - Webshell patterns
   - Registry persistence
   - Network activity

2. **crypto_miners.yar**
   - Cryptocurrency miner strings
   - Mining pool connections
   - Bitcoin wallet addresses

**Custom Rules**:
Add your own `.yar` files to `config/yara/` directory

### 4. Interactive Dashboard

#### Statistics Cards
- **Total Cases**: Number of investigations
- **Files Analyzed**: Cumulative file count
- **High Entropy**: Suspicious files detected
- **YARA Matches**: Malware detections

#### Recent Cases View
- Sortable case list
- Threat level badges
- Quick access to reports
- Auto-refresh every 30 seconds

### 5. Comprehensive Reports

#### Visual Analytics
**Charts Included**:
1. **Findings Distribution** (Pie Chart)
   - High entropy files
   - Executables
   - YARA matches
   - Clean files

2. **Entropy Distribution** (Bar Chart)
   - Histogram of entropy values
   - Identifies clustering patterns
   - Highlights anomalies

#### Detailed Findings Table
**Columns**:
- File path
- SHA256 hash (truncated)
- Entropy score
- Threat flags
- Action buttons

**Features**:
- Color-coded rows (red = dangerous, yellow = suspicious)
- Sortable columns
- Threat intelligence lookup
- Export capabilities

### 6. Threat Intelligence Integration

#### Mock API (Ready for Integration)
Current implementation provides sample data for:
- Threat level assessment
- Detection counts
- First/last seen dates
- Tags and classifications
- Recommendations

#### Ready for Real Integration
Easily connect to:
- **VirusTotal API**: File reputation lookup
- **AlienVault OTX**: Open threat exchange
- **Hybrid Analysis**: Malware sandbox
- **MISP**: Threat intelligence sharing

**Integration Points**:
- `/api/threat-intel/<hash>` endpoint
- Modify `app.py` to add real API calls
- Add API keys to configuration

### 7. Modern UI/UX

#### Design Features
- **Gradient Backgrounds**: Purple-blue theme
- **Smooth Animations**: Hover effects, transitions
- **Responsive Layout**: Mobile-friendly design
- **Bootstrap 5**: Modern component library
- **Bootstrap Icons**: Comprehensive icon set

#### User Experience
- **One-Click Actions**: Start scans easily
- **Live Updates**: Real-time progress
- **Intuitive Navigation**: Clear menu structure
- **Print-Friendly Reports**: Professional output

### 8. API Endpoints

#### Available APIs
```
GET  /                          - Dashboard
GET  /scan                      - Scan initiation page
GET  /report/<case_id>          - Case report view
GET  /api/cases                 - List all cases (JSON)
GET  /api/report/<case_id>      - Get case data (JSON)
GET  /api/stats                 - Dashboard statistics (JSON)
POST /api/scan                  - Initiate new scan
GET  /api/scan/<id>/status      - Check scan progress
GET  /api/threat-intel/<hash>   - Threat intelligence lookup
```

#### API Usage Examples

**Start a scan**:
```javascript
fetch('/api/scan', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        target: 'C:\\Path\\To\\Scan',
        scan_type: 'quick'
    })
})
```

**Check scan status**:
```javascript
fetch('/api/scan/scan_1234567890/status')
    .then(res => res.json())
    .then(data => console.log(data.status))
```

**Get case statistics**:
```javascript
fetch('/api/stats')
    .then(res => res.json())
    .then(stats => {
        console.log(`Total cases: ${stats.total_cases}`);
        console.log(`Threats: ${stats.yara_matches}`);
    })
```

## Configuration Options

### config/default.yaml

```yaml
app:
  name: Cyber Triage Tool
  version: 0.1.0
  output_dir: data/cases        # Report output directory
  log_dir: logs                 # Log file directory
  web:
    host: 127.0.0.1            # Web server host
    port: 8000                 # Web server port
    debug: false               # Debug mode

triage:
  quick_scan:
    max_file_size_mb: 50       # Maximum file size to analyze
    yara_rules_dir: config/yara # YARA rules location
  full_analysis:
    enable_memory_analysis: true
    network_scan_timeout: 10

investigation:
  default_case_prefix: CASE     # Case ID prefix
  evidence_dirs:
    - data/evidence

logging:
  level: INFO                   # DEBUG, INFO, WARNING, ERROR
  format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
  file: logs/app.log
```

## Performance Optimization

### Current Implementation
- **Streaming I/O**: 1MB chunks for memory efficiency
- **Fast PE Loading**: Minimal parsing for speed
- **Configurable Limits**: File size restrictions
- **Background Processing**: Non-blocking scans

### Future Enhancements
- Multi-threaded file processing
- Result caching
- Database indexing
- Incremental scanning

## Security Considerations

### Built-in Security
- ✅ Localhost binding by default
- ✅ File size limits
- ✅ Symlink protection
- ✅ Error handling
- ✅ Input validation

### Production Recommendations
- 🔐 Add authentication (Flask-Login, OAuth)
- 🔐 Enable HTTPS (SSL/TLS)
- 🔐 Implement rate limiting
- 🔐 Add CSRF protection
- 🔐 Use environment variables for secrets
- 🔐 Enable audit logging

## Extensibility

### Adding Custom Analyzers
1. Create new file in `src/analyzers/`
2. Implement `analyze_file(path)` function
3. Import in `triage_engine.py`
4. Add to analysis pipeline

### Adding Custom YARA Rules
1. Create `.yar` file in `config/yara/`
2. Follow YARA syntax
3. Rules auto-loaded on scan

### Adding API Endpoints
1. Add route in `src/web/app.py`
2. Implement handler function
3. Return JSON response
4. Update documentation

## Troubleshooting

### Common Issues

**Issue**: High memory usage
- **Solution**: Reduce `max_file_size_mb` in config
- **Solution**: Process fewer files per scan

**Issue**: Slow scans
- **Solution**: Exclude large directories
- **Solution**: Increase file size limit
- **Solution**: Disable YARA for quick scans

**Issue**: YARA rules not loading
- **Solution**: Check file permissions
- **Solution**: Verify YARA syntax
- **Solution**: Check `yara_rules_dir` path

**Issue**: Web interface not accessible
- **Solution**: Check firewall settings
- **Solution**: Verify port availability
- **Solution**: Check logs for errors

## Best Practices

### Scanning
1. Start with quick scans for triage
2. Run full analysis on suspicious findings
3. Regularly update YARA rules
4. Document investigation findings

### Analysis
1. Always investigate YARA matches
2. Check high-entropy files manually
3. Verify executable legitimacy
4. Cross-reference with threat intelligence

### Reporting
1. Export reports for documentation
2. Archive case data regularly
3. Track trends over time
4. Share findings with team

---

**For more information, see [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)**
