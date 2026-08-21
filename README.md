# python-security-tools

**Python & Bash Security Tools** — A collection of security utilities built for learning, demonstration, and practical use. Each tool includes a README explaining what it does, how to run it, and what security concept it demonstrates.

> These tools are for educational and authorized use only.

---

## Tools

| Tool | Language | Description |
|---|---|---|
| `port-scanner` | Python | TCP port scanner for host reconnaissance — scans a range, identifies open services |
| `dict-attack-demo` | Python | Dictionary-based credential attack demonstration — shows why strong passwords matter |
| `password-validator` | Python | Evaluates password strength against length, complexity, entropy, and common patterns |
| `caesar-cipher` | Python | Caesar cipher with encode, decode, and brute-force break modes |
| `packet-sniffer` | Python/Scapy | Live network traffic capture and protocol analysis — mirrors SOC monitoring workflows |
| `todo-manager` | Python | Command-line task manager with persistent storage and OOP structure |
| `snake-water-gun` | Python | Classic game demonstrating Python fundamentals, input handling, and game logic |
| `logpattern-analyzer` | Bash | Log parser scanning for configurable patterns with timestamp and frequency output |

---

## Requirements

```bash
pip install scapy        # for packet-sniffer
```

All other tools use Python 3 standard library only.

---

## Usage

Each tool has its own folder with a dedicated README. Navigate into the folder and follow its instructions.

```bash
cd port-scanner
python3 scanner.py --target 192.168.1.1 --range 1-1024
```

---

## Disclaimer

The dictionary attack demo and packet sniffer are for educational and authorized testing purposes only. Do not use against systems you do not own or have explicit permission to test.

---

## Author

**Awais Ahmed** — Security Operations Analyst | DFIR Practitioner  
[Portfolio](https://awais-sec.github.io) · [LinkedIn](https://www.linkedin.com/in/awais-sec/)
