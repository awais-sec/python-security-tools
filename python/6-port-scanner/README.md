# Python TCP Port Scanner

A simple and beginner-friendly TCP port scanner written in Python using only the standard library.

The tool checks whether TCP ports on a target are open, closed, or unavailable due to a timeout. It also displays the common service name associated with each port when available.

> Use this tool only against systems you own or have explicit permission to test.

## Features

- Scan individual TCP ports
- Scan multiple ports
- Scan port ranges
- Scan all TCP ports from 1 to 65535
- Display common service names
- Configurable connection timeout
- Supports IP addresses and hostnames
- Interactive mode for beginners
- Command-line mode for faster use
- Uses only Python's standard library

## Requirements

- Python 3.8 or newer
- No external packages required

## Installation

Clone the repository or download `port_scanner.py`.

Then run:

```bash
python port_scanner.py
