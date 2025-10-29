from flask import Flask, render_template, abort, jsonify, request, send_file
from flask_socketio import SocketIO, emit
from pathlib import Path
import json
import logging
import threading
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# Global variable to track scan progress
scan_progress = {}


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cyber-triage-secret-key-change-in-production'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching in development
    socketio = SocketIO(app, cors_allowed_origins="*")

    CASES_DIR = Path(__file__).parent.parent.parent / "data/cases"
    CASES_DIR.mkdir(parents=True, exist_ok=True)

    @app.route("/")
    @app.route("/dashboard")  # Alternative route to bypass cache
    def index():
        """Main dashboard page"""
        try:
            cases = sorted(
                [d.name for d in CASES_DIR.iterdir() if d.is_dir()],
                reverse=True
            )
        except FileNotFoundError:
            cases = []
        return render_template("index.html", cases=cases)
    
    @app.route("/new-dashboard")
    def new_dashboard():
        """New dashboard with delete buttons (cache-free)"""
        return render_template("dashboard_new.html")

    @app.route("/scan")
    @app.route("/newscan")  # Alternative route to bypass cache
    def scan_page():
        """Scan initiation page"""
        return render_template("scan.html")

    @app.route("/report/<case_id>")
    def report(case_id):
        """Individual case report page"""
        report_path = CASES_DIR / case_id / "report.json"
        if not report_path.exists():
            abort(404, description="Report not found")
        
        with open(report_path) as f:
            data = json.load(f)
            summary = data.get("summary", {})
            
        return render_template("report_new.html", summary=summary, case_id=case_id)

    @app.route("/api/cases")
    def api_cases():
        """API endpoint to list all cases"""
        try:
            cases = []
            for case_dir in sorted(CASES_DIR.iterdir(), reverse=True):
                if case_dir.is_dir():
                    report_path = case_dir / "report.json"
                    if report_path.exists():
                        with open(report_path) as f:
                            data = json.load(f)
                            summary = data.get("summary", {})
                            cases.append({
                                "id": case_dir.name,
                                "target": summary.get("target", "Unknown"),
                                "count": summary.get("count", 0),
                                "generated_at": summary.get("generated_at", "")
                            })
            return jsonify({"cases": cases})
        except Exception as e:
            logger.error(f"Error listing cases: {e}")
            return jsonify({"cases": [], "error": str(e)})

    @app.route("/api/report/<case_id>")
    def report_data(case_id):
        """API endpoint to get case report data"""
        report_path = CASES_DIR / case_id / "report.json"
        if not report_path.exists():
            abort(404)
            
        with open(report_path) as f:
            data = json.load(f)
            
        return jsonify(data)

    @app.route("/api/stats")
    def api_stats():
        """API endpoint for dashboard statistics"""
        try:
            total_cases = 0
            total_files = 0
            high_entropy_files = 0
            executables = 0
            yara_matches = 0
            
            for case_dir in CASES_DIR.iterdir():
                if case_dir.is_dir():
                    report_path = case_dir / "report.json"
                    if report_path.exists():
                        total_cases += 1
                        with open(report_path) as f:
                            data = json.load(f)
                            items = data.get("items", [])
                            total_files += len(items)
                            
                            for item in items:
                                flags = item.get("flags", [])
                                if "high_entropy" in flags:
                                    high_entropy_files += 1
                                if "executable" in flags:
                                    executables += 1
                                if "yara_match" in flags:
                                    yara_matches += 1
            
            return jsonify({
                "total_cases": total_cases,
                "total_files": total_files,
                "high_entropy_files": high_entropy_files,
                "executables": executables,
                "yara_matches": yara_matches
            })
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return jsonify({"error": str(e)})

    @app.route("/api/scan", methods=["POST"])
    def api_scan():
        """API endpoint to initiate a scan"""
        data = request.get_json()
        target_path = data.get("target")
        scan_type = data.get("scan_type", "quick")
        
        if not target_path:
            return jsonify({"error": "Target path required"}), 400
        
        # Import here to avoid circular imports
        from ..utils.config import load_config
        from ..triage_engine import TriageEngine
        
        try:
            config = load_config("config/default.yaml")
            engine = TriageEngine(config, str(CASES_DIR))
            
            # Run scan in background thread
            scan_id = f"scan_{int(time.time())}"
            scan_progress[scan_id] = {"status": "running", "progress": 0}
            
            def run_scan():
                try:
                    case_dir = engine.quick_scan(target_path)
                    scan_progress[scan_id] = {
                        "status": "completed",
                        "progress": 100,
                        "case_id": case_dir.name
                    }
                except Exception as e:
                    logger.error(f"Scan error: {e}")
                    scan_progress[scan_id] = {
                        "status": "error",
                        "progress": 0,
                        "error": str(e)
                    }
            
            thread = threading.Thread(target=run_scan)
            thread.daemon = True
            thread.start()
            
            return jsonify({"scan_id": scan_id, "status": "started"})
        except Exception as e:
            logger.error(f"Error starting scan: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/scan/<scan_id>/status")
    def api_scan_status(scan_id):
        """API endpoint to check scan status"""
        if scan_id in scan_progress:
            return jsonify(scan_progress[scan_id])
        return jsonify({"error": "Scan not found"}), 404

    @app.route("/api/threat-intel/<file_hash>")
    def api_threat_intel(file_hash):
        """API endpoint for threat intelligence (mock data for now)"""
        # This would integrate with VirusTotal, AlienVault OTX, etc.
        return jsonify({
            "hash": file_hash,
            "threat_level": "medium",
            "detections": 3,
            "total_scans": 70,
            "first_seen": "2024-01-15",
            "last_seen": "2025-10-12",
            "tags": ["suspicious", "packed"],
            "recommendation": "Investigate further. File shows signs of packing/obfuscation."
        })

    @app.route("/api/case/<case_id>", methods=["DELETE"])
    def api_delete_case(case_id):
        """API endpoint to delete a case"""
        try:
            import shutil
            case_dir = CASES_DIR / case_id
            if not case_dir.exists():
                return jsonify({"error": "Case not found"}), 404
            
            # Delete the entire case directory
            shutil.rmtree(case_dir)
            logger.info(f"Deleted case: {case_id}")
            return jsonify({"success": True, "message": f"Case {case_id} deleted"})
        except Exception as e:
            logger.error(f"Error deleting case {case_id}: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/cases/clear-all", methods=["DELETE"])
    def api_clear_all_cases():
        """API endpoint to delete all cases"""
        try:
            import shutil
            deleted_count = 0
            
            for case_dir in CASES_DIR.iterdir():
                if case_dir.is_dir():
                    shutil.rmtree(case_dir)
                    deleted_count += 1
                    logger.info(f"Deleted case: {case_dir.name}")
            
            return jsonify({
                "success": True, 
                "message": f"Deleted {deleted_count} case(s)",
                "count": deleted_count
            })
        except Exception as e:
            logger.error(f"Error clearing all cases: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/browse")
    def api_browse():
        """API endpoint to browse directories"""
        try:
            import os
            path = request.args.get("path", "")
            
            # If no path provided, return drives on Windows
            if not path:
                if os.name == 'nt':  # Windows
                    import string
                    drives = []
                    for letter in string.ascii_uppercase:
                        drive = f"{letter}:\\"
                        if os.path.exists(drive):
                            drives.append({
                                "name": drive,
                                "path": drive,
                                "type": "drive"
                            })
                    return jsonify({"items": drives, "current_path": ""})
                else:  # Linux/Mac
                    path = "/"
            
            # List directories in the given path
            items = []
            try:
                for entry in os.scandir(path):
                    if entry.is_dir():
                        items.append({
                            "name": entry.name,
                            "path": entry.path,
                            "type": "directory"
                        })
            except PermissionError:
                return jsonify({"error": "Permission denied"}), 403
            
            # Sort directories alphabetically
            items.sort(key=lambda x: x["name"].lower())
            
            return jsonify({
                "items": items,
                "current_path": path
            })
        except Exception as e:
            logger.error(f"Error browsing: {e}")
            return jsonify({"error": str(e)}), 500

    return app, socketio


if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, debug=True, port=8000, allow_unsafe_werkzeug=True)