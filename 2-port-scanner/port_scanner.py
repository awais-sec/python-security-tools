import socket


def check_port(ip, port):
    """Check whether a port is open on the target IP address."""
    try:
        port = int(port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))

            if result == 0:
                print(f"Port {port} is open.")
            else:
                print(f"Port {port} is closed.")

    except ValueError:
        print(f"Invalid port '{port}': Port should be an integer.")
    except OSError as e:
        print(f"Error checking port {port}: {e}")


def scan_ports(ip, ports):
    """Check each port in the provided list."""
    for port in ports:
        check_port(ip, port)


def main():
    target_ip = input("Enter the target IP address: ").strip()
    ports = input("Enter a list of ports (comma-separated): ").split(",")
    ports = [port.strip() for port in ports]

    scan_ports(target_ip, ports)


if __name__ == "__main__":
    main()
