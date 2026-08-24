import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from scapy.all import sniff, wrpcap


captured_packets = []
sniffing = False
sniffing_thread = None


def handle_packet(packet):
    """Display and store a captured packet."""
    captured_packets.append(packet)
    log_text.after(0, add_packet_to_log, packet.summary())


def add_packet_to_log(summary):
    """Add a packet summary to the GUI log."""
    log_text.insert(tk.END, summary + "\n")
    log_text.see(tk.END)


def get_filter():
    """Return the Scapy filter selected by the user."""
    filters = {
        "All": "",
        "TCP": "tcp",
        "UDP": "udp",
        "ICMP": "icmp",
    }
    return filters[filter_var.get()]


def start_sniffing():
    """Start packet capture in a background thread."""
    global sniffing, sniffing_thread

    if sniffing:
        return

    captured_packets.clear()
    log_text.insert(tk.END, "Starting packet capture...\n")
    log_text.see(tk.END)

    packet_limit = limit_entry.get().strip()
    count = int(packet_limit) if packet_limit.isdigit() else 0

    sniffing = True
    sniffing_thread = threading.Thread(
        target=run_sniffer,
        args=(get_filter(), count),
        daemon=True,
    )
    sniffing_thread.start()


def run_sniffer(packet_filter, count):
    """Run Scapy's packet capture outside the GUI thread."""
    global sniffing

    try:
        sniff(
            prn=handle_packet,
            store=False,
            filter=packet_filter,
            count=count,
            stop_filter=lambda packet: not sniffing,
        )
    except Exception as error:
        log_text.after(0, show_sniff_error, str(error))
    finally:
        sniffing = False
        log_text.after(0, capture_finished)


def show_sniff_error(error):
    """Display a packet capture error."""
    messagebox.showerror("Capture Error", error)


def capture_finished():
    """Update the log when packet capture finishes."""
    log_text.insert(tk.END, "Packet capture stopped.\n")
    log_text.see(tk.END)


def stop_sniffing():
    """Request that the current packet capture stop."""
    global sniffing
    sniffing = False
    log_text.insert(tk.END, "Stopping packet capture...\n")
    log_text.see(tk.END)


def save_packets():
    """Save captured packets as a PCAP file and a text summary."""
    if not captured_packets:
        messagebox.showwarning("No Packets", "No packets have been captured yet.")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".pcap",
        filetypes=[("PCAP files", "*.pcap"), ("All files", "*.*")],
    )

    if not filename:
        return

    try:
        wrpcap(filename, captured_packets)

        text_filename = filename.rsplit(".", 1)[0] + ".txt"
        with open(text_filename, "w") as text_file:
            for packet in captured_packets:
                text_file.write(packet.summary() + "\n")

        messagebox.showinfo(
            "Saved",
            f"Packets saved to:\n{filename}\n\nSummaries saved to:\n{text_filename}",
        )
    except OSError as error:
        messagebox.showerror("Save Error", str(error))


def clear_log():
    """Clear the packet log and captured packet list."""
    captured_packets.clear()
    log_text.delete("1.0", tk.END)
    log_text.insert(tk.END, "Packet log cleared.\n")


root = tk.Tk()
root.title("Packet Sniffer")
root.geometry("750x500")

filter_frame = tk.LabelFrame(root, text="Packet Filter", padx=10, pady=10)
filter_frame.pack(padx=10, pady=10, fill="x")

filter_var = tk.StringVar(value="All")
for name in ("All", "TCP", "UDP", "ICMP"):
    tk.Radiobutton(
        filter_frame,
        text=f"{name} Packets" if name != "All" else "All Packets",
        variable=filter_var,
        value=name,
    ).pack(anchor="w")

limit_frame = tk.LabelFrame(root, text="Packet Limit", padx=10, pady=10)
limit_frame.pack(padx=10, pady=5, fill="x")

limit_entry = tk.Entry(limit_frame)
limit_entry.pack(fill="x")
limit_entry.insert(0, "0")

log_frame = tk.LabelFrame(root, text="Packet Log", padx=10, pady=10)
log_frame.pack(padx=10, pady=10, fill="both", expand=True)

log_text = tk.Text(log_frame, wrap=tk.WORD)
log_text.pack(fill="both", expand=True)

button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack(fill="x")

tk.Button(button_frame, text="Start Sniffing", command=start_sniffing).pack(side="left", padx=5)
tk.Button(button_frame, text="Stop Sniffing", command=stop_sniffing).pack(side="left", padx=5)
tk.Button(button_frame, text="Save to PCAP", command=save_packets).pack(side="left", padx=5)
tk.Button(button_frame, text="Clear Log", command=clear_log).pack(side="left", padx=5)

root.mainloop()
