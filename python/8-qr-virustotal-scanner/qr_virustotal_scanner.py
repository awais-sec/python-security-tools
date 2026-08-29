"""
QR Code Security Scanner with VirusTotal Integration
Scans QR codes and checks extracted URLs against VirusTotal for malicious links.
"""

import cv2
import requests
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import re
from datetime import datetime
import json

class QRVTScanner:
    """QR Code Scanner with VirusTotal malware detection."""
    
    def __init__(self, root, api_key=None):
        """
        Initialize the QR Scanner application.
        
        Args:
            root: Tkinter root window
            api_key: VirusTotal API key (optional)
        """
        self.root = root
        self.root.title("QR Code Security Scanner")
        self.root.geometry("900x700")
        self.api_key = api_key
        self.scanning = False
        self.camera_running = False
        self.scan_results = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Top frame for controls
        control_frame = ttk.LabelFrame(self.root, text="Scanner Controls", padding=10)
        control_frame.pack(padx=10, pady=10, fill="x")
        
        # API Key entry
        ttk.Label(control_frame, text="VirusTotal API Key:").pack(side="left", padx=5)
        self.api_key_entry = ttk.Entry(control_frame, width=40, show="*")
        self.api_key_entry.pack(side="left", padx=5)
        if self.api_key:
            self.api_key_entry.insert(0, self.api_key)
        
        # Buttons
        ttk.Button(control_frame, text="Start Camera", command=self.start_camera).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Stop Camera", command=self.stop_camera).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Scan from File", command=self.scan_file).pack(side="left", padx=5)
        
        # Camera frame
        camera_frame = ttk.LabelFrame(self.root, text="Live Camera Feed", padding=5)
        camera_frame.pack(padx=10, pady=10, fill="both", expand=False)
        
        self.camera_label = ttk.Label(camera_frame, text="Camera not started", background="gray", height=15)
        self.camera_label.pack(fill="both", expand=True)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.root, text="Scan Results", padding=10)
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Results text area with scrollbar
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=12, yscrollcommand=scrollbar.set)
        self.results_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.results_text.yview)
        
        # Bottom frame for actions
        action_frame = ttk.Frame(self.root, padding=10)
        action_frame.pack(fill="x")
        
        ttk.Button(action_frame, text="Clear Results", command=self.clear_results).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Export Results", command=self.export_results).pack(side="left", padx=5)
    
    def log_result(self, message):
        """Log a message to results text area."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def start_camera(self):
        """Start camera feed and QR scanning."""
        if self.camera_running:
            messagebox.showwarning("Camera", "Camera is already running")
            return
        
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("API Key Required", "Please enter your VirusTotal API key")
            return
        
        self.api_key = api_key
        self.camera_running = True
        self.scanning = True
        self.log_result("Starting camera feed...")
        
        thread = threading.Thread(target=self._camera_thread, daemon=True)
        thread.start()
    
    def _camera_thread(self):
        """Run camera scanning in separate thread."""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.log_result("❌ Error: Cannot access camera")
                self.camera_running = False
                return
            
            self.log_result("✓ Camera started")
            
            while self.scanning and self.camera_running:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Decode QR codes
                decoded_objects = decode(frame)
                
                # Draw on frame
                for obj in decoded_objects:
                    x, y, w, h = obj.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "QR Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Process QR data
                    qr_data = obj.data.decode('utf-8')
                    if self._is_url(qr_data):
                        self.log_result(f"\n📱 QR Code Detected: {qr_data}")
                        self.log_result("🔍 Scanning with VirusTotal...")
                        self._check_url_virustotal(qr_data)
                
                # Convert to RGB for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_pil.thumbnail((400, 300))
                
                # Update label
                photo = ImageTk.PhotoImage(frame_pil)
                self.camera_label.config(image=photo)
                self.camera_label.image = photo
        
        except Exception as e:
            self.log_result(f"❌ Camera Error: {e}")
        
        finally:
            cap.release()
            self.camera_running = False
            self.camera_label.config(text="Camera stopped", image="")
            self.log_result("Camera closed")
    
    def stop_camera(self):
        """Stop camera feed."""
        self.scanning = False
        self.camera_running = False
        self.log_result("Stopping camera...")
    
    def scan_file(self):
        """Scan QR code from file."""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("API Key Required", "Please enter your VirusTotal API key")
            return
        
        self.api_key = api_key
        
        file_path = filedialog.askopenfilename(
            title="Select QR Code Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.log_result(f"\n📁 Scanning file: {file_path}")
        
        thread = threading.Thread(target=self._scan_file_thread, args=(file_path,), daemon=True)
        thread.start()
    
    def _scan_file_thread(self, file_path):
        """Scan QR code from file in separate thread."""
        try:
            image = cv2.imread(file_path)
            decoded_objects = decode(image)
            
            if not decoded_objects:
                self.log_result("❌ No QR code found in image")
                return
            
            self.log_result(f"✓ Found {len(decoded_objects)} QR code(s)")
            
            for i, obj in enumerate(decoded_objects, 1):
                qr_data = obj.data.decode('utf-8')
                self.log_result(f"\nQR Code #{i}: {qr_data}")
                
                if self._is_url(qr_data):
                    self.log_result("🔍 Scanning with VirusTotal...")
                    self._check_url_virustotal(qr_data)
                else:
                    self.log_result("ℹ️ Data is not a URL, skipping VirusTotal check")
        
        except Exception as e:
            self.log_result(f"❌ File Scan Error: {e}")
    
    def _is_url(self, string):
        """Check if string is a valid URL."""
        url_pattern = re.compile(
            r'^https?://'  # http or https
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)*[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(string) is not None
    
    def _check_url_virustotal(self, url):
        """Check URL against VirusTotal API."""
        try:
            # Encode URL
            url_id = self._get_url_id(url)
            
            # API endpoint
            headers = {"x-apikey": self.api_key}
            response = requests.get(
                f"https://www.virustotal.com/api/v3/urls/{url_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 401:
                self.log_result("❌ Invalid VirusTotal API key")
                return
            
            if response.status_code != 200:
                self.log_result(f"❌ VirusTotal API error: {response.status_code}")
                return
            
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            undetected = stats.get("undetected", 0)
            harmless = stats.get("harmless", 0)
            
            # Display results
            self.log_result("=" * 60)
            self.log_result(f"📊 VirusTotal Analysis Results:")
            self.log_result(f"   ✅ Harmless: {harmless}")
            self.log_result(f"   ⚠️  Suspicious: {suspicious}")
            self.log_result(f"   🚫 Malicious: {malicious}")
            self.log_result(f"   ❓ Undetected: {undetected}")
            
            # Safety verdict
            if malicious > 0:
                self.log_result(f"\n   🚨 ALERT: URL is MALICIOUS! ({malicious} vendors detected)")
                messagebox.showerror("⚠️ MALICIOUS URL DETECTED", 
                    f"This URL is flagged as malicious by {malicious} security vendors!")
            elif suspicious > 0:
                self.log_result(f"\n   ⚠️ WARNING: URL is SUSPICIOUS! ({suspicious} vendors detected)")
                messagebox.showwarning("⚠️ SUSPICIOUS URL", 
                    f"This URL is flagged as suspicious by {suspicious} vendors. Use caution!")
            else:
                self.log_result(f"\n   ✅ SAFE: URL appears to be safe")
                messagebox.showinfo("✓ Safe URL", "This URL appears to be safe!")
            
            self.log_result("=" * 60)
            
            # Store result
            self.scan_results.append({
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "malicious": malicious,
                "suspicious": suspicious,
                "harmless": harmless
            })
        
        except requests.exceptions.Timeout:
            self.log_result("❌ VirusTotal request timeout")
        except requests.exceptions.RequestException as e:
            self.log_result(f"❌ Network error: {e}")
        except Exception as e:
            self.log_result(f"❌ Error checking URL: {e}")
    
    def _get_url_id(self, url):
        """Convert URL to VirusTotal URL ID."""
        import base64
        return base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
    
    def clear_results(self):
        """Clear results text area."""
        self.results_text.delete(1.0, tk.END)
        self.scan_results.clear()
        self.log_result("Results cleared")
    
    def export_results(self):
        """Export scan results to JSON file."""
        if not self.scan_results:
            messagebox.showwarning("No Results", "No scan results to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self.scan_results, f, indent=2)
            self.log_result(f"✓ Results exported to {file_path}")
            messagebox.showinfo("Success", f"Results exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = QRVTScanner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
