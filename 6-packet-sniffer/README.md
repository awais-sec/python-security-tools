# Packet Sniffer

A Python packet-capture tool built with Scapy and Tkinter. It provides a simple graphical interface for capturing packets, filtering common protocols, viewing packet summaries, and saving captures for later analysis.

## What It Does

- Captures network packets using Scapy.
- Supports All, TCP, UDP, and ICMP filters.
- Allows the user to set a packet limit.
- Displays packet summaries in the GUI.
- Saves captured packets as a PCAP file.
- Saves packet summaries to a text file.

## Why It Is a Security Tool

Packet capture is an important network-security and troubleshooting technique. Security analysts can use packet captures to investigate network activity, understand protocols, and support incident analysis.

> Only capture traffic on systems and networks that you own or have explicit permission to monitor. Captured traffic may contain sensitive information.

## Requirements

- Python 3
- Scapy
- Tkinter
- Appropriate permissions for packet capture on the operating system

Install Scapy with:

```bash
pip install scapy
```

Tkinter is normally included with standard Python installations on Windows. Linux users may need to install their distribution's Tk package separately.

## Usage

Run the script:

```bash
python packet_sniffer.py
```

The application provides:

1. **Packet Filter** — choose All, TCP, UDP, or ICMP traffic.
2. **Packet Limit** — enter the number of packets to capture. Use `0` for continuous capture until stopped.
3. **Start Sniffing** — begin the capture.
4. **Stop Sniffing** — request that the capture stop.
5. **Save to PCAP** — save captured packets and a text summary.
6. **Clear Log** — clear the displayed packet summaries and stored capture.

## How It Works

Scapy performs the packet capture while the Tkinter interface displays packet summaries. The capture runs in a background thread so the GUI remains responsive while packets are being collected.

Captured packets are kept in memory until the user saves or clears them.

## Limitations

- Packet capture capabilities depend on the operating system and available network interfaces.
- Some systems require elevated privileges for packet capture.
- The tool displays packet summaries rather than providing a full protocol-analysis interface.
- It does not decrypt encrypted network traffic.
- It does not provide advanced filtering or deep packet inspection.
- Continuous capture can consume memory if packets are not saved or cleared.

## Skills Demonstrated

- Python socket/network-security concepts
- Scapy packet capture
- Protocol filtering
- Tkinter GUI development
- Threading
- PCAP file handling
- Basic network monitoring
