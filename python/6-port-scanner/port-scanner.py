import socket
import argparse


def get_service_name(port):
    """Get the common service name for a port."""
    try:
        return socket.getservbyport(port, "tcp").upper()
    except OSError:
        return "UNKNOWN"


def parse_ports(port_input):
    """Convert port input into a sorted list of port numbers."""
    ports = set()

    for item in port_input.split(","):
        item = item.strip()

        try:
            # Handle a port range, for example: 20-25
            if "-" in item:
                start, end = item.split("-", 1)
                start = int(start)
                end = int(end)

                if start > end:
                    raise ValueError

                for port in range(start, end + 1):
                    if 1 <= port <= 65535:
                        ports.add(port)
                    else:
                        print(f"Port out of range: {port}")

            # Handle a single port
            else:
                port = int(item)

                if 1 <= port <= 65535:
                    ports.add(port)
                else:
                    print(f"Port out of range: {port}")

        except ValueError:
            print(f"Invalid port: {item}")

    return sorted(ports)


def check_port(target, port, timeout):
    """Check whether a TCP port is open, closed, or timed out."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)

            result = sock.connect_ex((target, port))

            if result == 0:
                return "OPEN"

            return "CLOSED"

    except socket.timeout:
        return "TIMEOUT"

    except OSError:
        return "ERROR"


def scan_ports(target, ports, timeout):
    """Scan all specified ports on the target."""
    print("\nPort Scanner")
    print("=" * 45)
    print(f"Target: {target}")
    print(f"Ports:  {len(ports)}")
    print("=" * 45)

    print(f"{'PORT':<8}{'SERVICE':<15}{'STATUS'}")
    print("-" * 45)

    for port in ports:
        status = check_port(target, port, timeout)
        service = get_service_name(port)

        print(f"{port:<8}{service:<15}{status}")


def main():
    parser = argparse.ArgumentParser(
        description="Simple TCP port scanner for authorized security testing."
    )

    parser.add_argument(
        "target",
        nargs="?",
        help="Target IP address or hostname"
    )

    parser.add_argument(
        "-p",
        "--ports",
        help="Ports to scan, e.g. 22,80,443 or 1-100"
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=1.0,
        help="Connection timeout in seconds (default: 1)"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan all TCP ports from 1 to 65535"
    )

    args = parser.parse_args()

    # Interactive mode
    if not args.target:
        args.target = input("Enter target IP address or hostname: ").strip()

    if not args.ports and not args.all:
        args.ports = input(
            "Enter ports to scan (e.g. 22,80,443 or 1-100): "
        ).strip()

        if args.ports.lower() == "all":
            args.all = True

    # Scan all ports
    if args.all:
        ports = list(range(1, 65536))

    # Scan selected ports
    else:
        ports = parse_ports(args.ports)

    if not ports:
        print("No valid ports were provided.")
        return

    # Check whether the target can be resolved
    try:
        socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"Could not resolve target: {args.target}")
        return

    scan_ports(args.target, ports, args.timeout)

    print("\nScan complete.")


if __name__ == "__main__":
    main()
