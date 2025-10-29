import os

def generate_connections_file():
    connections = [
        # User Interface Layer
        {"from": "User", "to": "Web UI", "data": "Login/Interact, Commands"},
        {"from": "User", "to": "CLI", "data": "Commands, API Key"},
        
        # Authentication Flows
        {"from": "Web UI", "to": "Authentication", "data": "Auth Request"},
        {"from": "CLI", "to": "Authentication", "data": "API Key"},
        {"from": "Authentication", "to": "API Server", "data": "Auth Token"},
        
        # Core Processing
        {"from": "API Server", "to": "File System", "data": "File Operations"},
        {"from": "File System", "to": "Entropy Analysis", "data": "File Data"},
        {"from": "File System", "to": "PE Analyzer", "data": "PE Files"},
        {"from": "File System", "to": "YARA Scanner", "data": "Files to Scan"},
        
        # Analysis Results
        {"from": "Entropy Analysis", "to": "API Server", "data": "Results"},
        {"from": "PE Analyzer", "to": "API Server", "data": "Results"},
        {"from": "YARA Scanner", "to": "API Server", "data": "Results"},
        
        # Reporting
        {"from": "API Server", "to": "Report Generator", "data": "Analysis Data"},
        {"from": "Report Generator", "to": "API Server", "data": "Generated Reports"},
        
        # Data Storage
        {"from": "API Server", "to": "Database", "data": "Store Results"},
        {"from": "Database", "to": "API Server", "data": "Retrieve Data"},
        
        # Response Paths
        {"from": "API Server", "to": "Web UI", "data": "Responses, Reports"},
        {"from": "API Server", "to": "CLI", "data": "Command Output, Results"}
    ]
    
    # Create markdown content
    markdown = """# Cyber Triage Tool - System Flow Connections

## Connection List

| From | To | Data Flow |
|------|----|-----------|
"""
    for conn in connections:
        markdown += f"| {conn['from']} | {conn['to']} | {conn['data']} |\n"
    
    # Add description
    markdown += """
## Description of Components

### User Interface Layer
- **User**: The end user interacting with the system
- **Web UI**: Web-based interface for the application
- **CLI**: Command Line Interface for advanced users

### Processing Layer
- **Authentication**: Handles user authentication and authorization
- **API Server**: Central processing unit for all requests

### Analysis Components
- **Entropy Analysis**: Analyzes file entropy for encryption/packing detection
- **PE Analyzer**: Analyzes Portable Executable files
- **YARA Scanner**: Scans files using YARA rules

### Data Layer
- **File System**: Stores and retrieves files for analysis
- **Database**: Stores analysis results and system data

### Reporting
- **Report Generator**: Creates reports from analysis results
"""

    # Write to file
    output_path = os.path.join('d:\\BE Major Project All\\my choice\\cyber-triage-tool\\docs', 
                              'system_flow_connections.md')
    
    with open(output_path, 'w') as f:
        f.write(markdown)
    
    print(f"System flow connections saved as: {output_path}")

if __name__ == "__main__":
    generate_connections_file()