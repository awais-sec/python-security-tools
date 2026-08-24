from scapy.all import sniff, wrpcap
import tkinter as tk
from tkinter import messagebox, filedialog
import threading


packet_filter = ""
sniffing_thread = None
stop_sniffing_flag = False
captured_packets = []


def handle_packet(packet):
    """Display a captured packet and keep it for saving."""
    packet_summary = packet.summary()
    log_text.insert(tk.END, f"{packet_summary}\n")
    log_text.see(tk.END)
    captured_packets.append(packet)


def start_sniffing():
    """Start packet capture using the selected filter and packet limit."""
    global sniffing_thread, packet_filter, stop_sniffing_flag

    stop_sniffing_flag = False
    captured_packets.clear()

    filter_type = filter_var.get()

    if filter_type == "TCP":
        packet_filter = "tcp"
    elif filter_type == "UDP":
        packet_filter = "udp"
    elif filter_type == "ICMP":
        packet_filter = "icmp"
    else:
        packet_filter = ""

    limit = limit_entry.get()
    limit = int(limit) if limit.isdigit() else 0

    log_text.insert(tk.END, "Starting network packet sniffing...\n")
    log_text.see(tk.END)

    sniffing_thread = threading.Thread(
        target=lambda: sniff(
            prn=handle_packet,
            store=0,
            filter=packet_filter,
            count=limit,
            stop_filter=lambda packet: stop_sniffing_flag,
        )
    )
    sniffing_thread.start()


def stop_sniffing():
    """Request that the current packet capture stop."""
    global stop_sniffing_flag

    stop_sniffing_flag = True

    if sniffing_thread and sniffing_thread.is_alive():
        sniffing_thread.join(timeout=1)

    log_text.insert(tk.END, "Packet sniffing stopped.\n")
    log_text.see(tk.END)


def save_to_pcap_and_text():
    """Save captured packets to a PCAP file and text summaries."""
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
        messagebox.showinfo("Success", f"Packets saved to {filename}.")
    except OSError as error:
        messagebox.showerror("Error", f"Failed to save PCAP file: {error}")
        return

    text_filename = filename.rsplit(".", 1)[0] + ".txt"

    try:
        with open(text_filename, "w") as text_file:
            for packet in captured_packets:
                text_file.write(f"{packet.summary()}\n")

        messagebox.showinfo(
            "Success",
            f"Packet summaries saved to {text_filename}.",
        )
    except OSError as error:
        messagebox.showerror(
            "Error",
            f"Failed to save packet summaries: {error}",
        )


def clear_log():
    """Clear the packet log and captured packets."""
    log_text.delete(1.0, tk.END)
    captured_packets.clear()
    log_text.insert(tk.END, "Packet log cleared.\n")
    log_text.see(tk.END)


root = tk.Tk()
root.title("Enhanced Packet Sniffer")

filter_frame = tk.LabelFrame(root, text="Filter Options", padx=10, pady=10)
filter_frame.pack(padx=10, pady=10, fill="x")

filter_var = tk.StringVar(value="All")
tk.Radiobutton(filter_frame, text="All Packets", variable=filter_var, value="All").pack(anchor="w")
tk.Radiobutton(filter_frame, text="TCP Packets", variable=filter_var, value="TCP").pack(anchor="w")
tk.Radiobutton(filter_frame, text="UDP Packets", variable=filter_var, value="UDP").pack(anchor="w")
tk.Radiobutton(filter_frame, text="ICMP Packets", variable=filter_var, value="ICMP").pack(anchor="w")

limit_frame = tk.LabelFrame(root, text="Packet Limit", padx=10, pady=10)
limit_frame.pack(padx=10, pady=10, fill="x")

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
tk.Button(button_frame, text="Save to PCAP and Text", command=save_to_pcap_and_text).pack(side="left", padx=5)
tk.Button(button_frame, text="Clear Log", command=clear_log).pack(side="left", padx=5)

root.mainloop()
