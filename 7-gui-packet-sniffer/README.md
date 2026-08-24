# GUI-based Packet Sniffer

A professional, graphical packet sniffer tool built with Python and Tkinter that captures and analyzes network packets with real-time filtering capabilities.

## Features

✅ **Real-time Packet Capture** - Live network packet sniffing with instant display
✅ **Protocol Filtering** - Filter packets by TCP, UDP, or ICMP protocols
✅ **Packet Limiting** - Set a limit on the number of packets to capture (0 = unlimited)
✅ **Dual Export Formats** - Save packets as PCAP files and text summaries
✅ **User-friendly GUI** - Intuitive interface with color-coded buttons
✅ **Scrollable Log** - View captured packets with auto-scroll functionality
✅ **Error Handling** - Comprehensive error messages and permission checks
✅ **Privilege Detection** - Alerts user if running without required privileges

## Requirements

### Python Packages
- `scapy` - Network packet manipulation library
- `tkinter` - GUI framework (usually included with Python)

### System Requirements
- **Administrator/Root privileges** (required for network packet capture)
- Python 3.6+
- Windows, Linux, or macOS

## Installation

### Step 1: Install Dependencies
```bash
pip install scapy
```

### Step 2: Ensure Admin/Root Privileges
- **Windows**: Run Command Prompt/PowerShell as Administrator
- **Linux/macOS**: Use `sudo` when running the script

## Usage

### Running the Application

**Windows (Administrator required):**
```bash
python packet_sniffer_gui.py
```

**Linux/macOS (Root required):**
```bash
sudo python packet_sniffer_gui.py
```

### GUI Controls

1. **Filter Options** - Select packet type:
   - All Packets (no filtering)
   - TCP Packets
   - UDP Packets
   - ICMP Packets

2. **Packet Limit** - Enter the number of packets to capture:
   - 0 = Unlimited (default)
   - Any positive integer = Capture that many packets

3. **Start Sniffing** - Begin capturing packets with selected filters

4. **Stop Sniffing** - Stop the capture process at any time

5. **Save Packets** - Export captured packets:
   - Creates a `.pcap` file (binary format, compatible with Wireshark)
   - Creates a `.txt` file (human-readable packet summaries)

6. **Clear Log** - Clear the log display and reset captured packets

## Key Improvements

### Fixed Issues
- ✅ Daemon thread support for clean application exit
- ✅ Enhanced error handling with specific messages
- ✅ Permission checking before attempting packet capture
- ✅ Better thread management and cleanup
- ✅ Improved button state management during capture
- ✅ UTF-8 encoding for text file exports
- ✅ Scrollbar support for large packet logs

### Code Quality
- ✅ Comprehensive docstrings for all functions
- ✅ Global state management
- ✅ Proper exception handling
- ✅ Color-coded UI buttons for better UX
- ✅ Informative status messages in the log

## Example Output

```
Starting packet capture (TCP)...
Ether / IP / TCP 192.168.1.100:54321 > 8.8.8.8:443 S
Ether / IP / TCP 8.8.8.8:443 > 192.168.1.100:54321 SA
Ether / IP / TCP 192.168.1.100:54321 > 8.8.8.8:443 A
Saved 3 packets to C:\Users\User\packets.pcap
Saved packet summaries to C:\Users\User\packets.txt
```

## Supported Filters

- **tcp** - Transmission Control Protocol
- **udp** - User Datagram Protocol
- **icmp** - Internet Control Message Protocol
- **(empty)** - All protocols

## Troubleshooting

### "Permission Denied" Error
**Solution**: Run with administrator/root privileges
- Windows: Right-click Command Prompt → Run as Administrator
- Linux/macOS: Prefix command with `sudo`

### "No module named 'scapy'" Error
**Solution**: Install scapy
```bash
pip install scapy
```

### No packets captured
**Solution**: 
- Check network connectivity
- Verify filter settings are correct
- Ensure active network traffic exists
- On Linux, check if using virtual interfaces (may require additional setup)

## Technical Details

### Threading Model
- Packet capture runs in a separate daemon thread
- GUI remains responsive during capture
- Graceful shutdown with timeout handling

### File Formats

**PCAP Format** (`.pcap`)
- Binary format compatible with Wireshark
- Contains full packet data
- Can be re-analyzed with other tools

**Text Format** (`.txt`)
- Human-readable packet summaries
- One line per packet
- Contains protocol and connection information

## Security Notes

⚠️ This tool requires elevated privileges to capture network traffic.
⚠️ Use only on networks you own or have permission to analyze.
⚠️ Packet capture can expose sensitive information in network traffic.

## Author

Created as an educational tool for network analysis and packet inspection.

## License

This project is provided for educational purposes. Modify and use as needed.
