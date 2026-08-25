# QR Code Security Scanner with VirusTotal Integration

A powerful security tool that scans QR codes and checks extracted URLs against VirusTotal's malware detection database to identify malicious links.

## Features

✅ **Live QR Code Scanning** - Real-time QR code detection from camera feed
✅ **File-based Scanning** - Scan QR codes from image files (PNG, JPG, BMP, GIF)
✅ **VirusTotal Integration** - Check URLs against VirusTotal's malware database
✅ **Detailed Threat Analysis** - Shows malicious, suspicious, harmless, and undetected counts
✅ **Real-time Alerts** - Immediate notification of malicious/suspicious URLs
✅ **Scan History** - Track all scanned URLs and results
✅ **Export Results** - Save scan results to JSON for reporting
✅ **User-friendly GUI** - Intuitive Tkinter interface
✅ **Threading** - Non-blocking operations with responsive UI

## Security Benefits

🛡️ **Protect Against Phishing** - Identifies phishing URLs embedded in QR codes
🛡️ **Malware Detection** - Detects URLs known to distribute malware
🛡️ **Credential Theft Prevention** - Warns about suspicious authentication URLs
🛡️ **Safe QR Code Scanning** - Never blindly open URLs from QR codes again
🛡️ **Compliance Ready** - Export reports for security audits

## Requirements

### Python Packages
- `opencv-python` - Camera and image processing
- `pyzbar` - QR code decoding
- `pillow` - Image handling
- `requests` - HTTP requests to VirusTotal API
- `tkinter` - GUI framework (usually included)

### System Requirements
- Python 3.6+
- Webcam for live scanning (optional, can scan files too)
- VirusTotal API Key (free tier available)
- Windows, Linux, or macOS

## Installation

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2: Get VirusTotal API Key

1. Visit: https://www.virustotal.com/gui/home/upload
2. Create a free account or sign in
3. Go to Settings → API key
4. Copy your API key

### Step 3: Run the Application
```bash
python qr_virustotal_scanner.py
```

## Usage Guide

### Live Camera Scanning

1. Launch the application
2. Enter your VirusTotal API Key
3. Click **"Start Camera"**
4. Point camera at QR codes
5. The app automatically scans and checks URLs
6. View results in real-time

### File-based Scanning

1. Click **"Scan from File"**
2. Select an image containing a QR code
3. The app extracts and checks the URL
4. View results immediately

### Understanding Results

**Verdict Indicators:**
- 🚨 **MALICIOUS** (Red) - URL is flagged by multiple security vendors
- ⚠️ **SUSPICIOUS** (Yellow) - URL is flagged by some vendors, use caution
- ✅ **SAFE** (Green) - URL passed all security checks
- ❓ **UNDETECTED** - Not enough data for verdict

**Analysis Stats:**
- Harmless: Number of vendors that flagged as safe
- Suspicious: Number of vendors with suspicious verdict
- Malicious: Number of vendors that flagged as malicious
- Undetected: Vendors that haven't analyzed yet

### Exporting Results

1. Scan multiple QR codes
2. Click **"Export Results"**
3. Save as JSON file
4. Use for security reports and audits

## API Key Security

⚠️ **Important Security Notes:**

- **Never commit API keys** to version control
- **Store keys in environment variables**: 
  ```bash
  set VIRUSTOTAL_API_KEY=your_key  # Windows
  export VIRUSTOTAL_API_KEY=your_key  # Linux/macOS
  ```
- **Free tier limits**: 4 requests/minute
- **Use responsibly** to avoid rate limiting

## Supported QR Code Data Types

- ✅ URLs (http, https)
- ✅ IP addresses
- ⚠️ Text (no VirusTotal check)
- ⚠️ Contact info (no VirusTotal check)
- ⚠️ WiFi credentials (not scanned for security)

## Troubleshooting

### "Camera not found"
**Solution**: Ensure webcam is connected and not in use by other applications

### "Invalid API Key"
**Solution**: 
- Verify your VirusTotal API key is correct
- Check key hasn't expired
- Create new key on VirusTotal website

### "QR code not detected"
**Solution**:
- Ensure good lighting
- Position QR code clearly in frame
- Try different angles
- Use high-quality image for file scanning

### "Rate limit exceeded"
**Solution**:
- Wait a minute before scanning again
- Upgrade to VirusTotal paid plan for higher limits
- Batch requests more efficiently

## Performance Tips

1. **Better Camera Quality** - Use high-resolution camera for faster detection
2. **Lighting** - Ensure adequate lighting for QR code recognition
3. **Distance** - Keep QR code 20-30cm from camera
4. **API Optimization** - Cache results to avoid repeated API calls

## Technical Details

### Threading Model
- UI runs on main thread for responsiveness
- Camera feed runs in background daemon thread
- VirusTotal API calls are non-blocking

### QR Code Processing
- Uses pyzbar for decoding
- Supports all QR code versions
- Handles multiple codes in single image

### VirusTotal API Integration
- Uses URL ID encoding (base64)
- Implements error handling for timeouts
- Rate limiting support

## Example Workflow

```
1. User starts camera → App initializes feed
2. User points at QR code → App detects QR
3. QR contains URL → App sends to VirusTotal
4. VirusTotal responds with analysis → App displays verdict
5. If malicious → Alert dialog appears
6. Results saved → User can export anytime
```

## Legal & Ethical

⚠️ **Use this tool responsibly:**
- Only scan QR codes you have permission to analyze
- Respect privacy of QR code owners
- Follow local laws regarding security testing
- Use for educational and protective purposes

## Author

Created as an educational security tool for QR code safety analysis.

## License

This project is provided for educational purposes. Modify and use as needed.

## Support

For issues or questions:
1. Check VirusTotal API status
2. Verify API key validity
3. Review camera permissions
4. Check Python version compatibility
