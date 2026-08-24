# Port Scanner

A simple Python TCP port scanner for checking whether selected ports are open or closed on a target IP address.

## What It Does

The tool:

- Takes a target IPv4 address from the user.
- Accepts a comma-separated list of ports.
- Attempts a TCP connection to each port.
- Reports whether each port is open or closed.
- Uses a short connection timeout so the scan does not wait indefinitely.

## Why It Is a Security Tool

Port scanning is a basic reconnaissance technique used to identify network services that may be reachable on a system. Security professionals can use this information to understand an exposed attack surface and identify ports that may need further investigation or restriction.

> Only scan systems and networks that you own or have explicit permission to test.

## Requirements

- Python 3
- No external packages are required.

## Usage

Run the script:

```bash
python port_scanner.py
```

Enter the target IP address and the ports to check:

```text
Enter the target IP address: 192.168.1.10
Enter a list of ports (comma-separated): 22,80,443,3389
```

Example output:

```text
Port 22 is open.
Port 80 is open.
Port 443 is closed.
Port 3389 is closed.
```

## How It Works

The scanner uses Python's built-in `socket` module and attempts a TCP connection to each supplied port.

A successful connection indicates that the port accepted the connection attempt. If the connection fails or times out, the tool reports the port as closed.

## Limitations

This is an intentionally simple learning tool. It:

- Checks only TCP ports.
- Scans only the ports supplied by the user.
- Does not identify the service or application behind an open port.
- Does not perform banner grabbing or service enumeration.
- Does not provide advanced scan types or stealth techniques.

## Skills Demonstrated

- Python socket programming
- TCP networking fundamentals
- Basic network reconnaissance
- Input handling and validation
- Connection timeouts
- Basic error handling
