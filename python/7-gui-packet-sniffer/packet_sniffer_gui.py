"""
Enhanced GUI-based Packet Sniffer
A graphical tool to capture and analyze network packets with filtering capabilities.
"""

from scapy.all import sniff, wrpcap
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import sys

# Global variables
packet_filter = ""
sniffing_thread = None
stop_sniffing_flag = False
captured_packets = []
is_sniffing = False


def handle_packet(packet):
    """
    Callback function to process each captured packet.
    
    Args:
        packet: The captured packet object (Scapy Packet instance).
    """
    try:
        packet_summary = packet.summary()
        log_text.insert(tk.END, f"{packet_summary}\n")
        log_text.see(tk.END)
        captured_packets.append(packet)
    except Exception as e:
        log_text.insert(tk.END, f"Error processing packet: {e}\n")
        log_text.see(tk.END)


def sniff_packets():
    """
    Execute packet sniffing in a separate thread.
    """
    global stop_sniffing_flag, is_sniffing
    
    try:
        is_sniffing = True
        update_button_states(sniffing=True)
        
        # Get packet limit
        limit = limit_entry.get()
        limit = int(limit) if limit.isdigit() and int(limit) > 0 else 0
        
        # Start sniffing
        sniff(
            prn=handle_packet,
            store=0,
            filter=packet_filter,
            count=limit if limit > 0 else 0,
            stop_filter=lambda x: stop_sniffing_flag,
            timeout=None
        )
    except PermissionError:
        log_text.insert(
            tk.END,
            "Error: This application requires administrator/root privileges to capture packets.\n"
        )
        log_text.see(tk.END)
        messagebox.showerror(
            "Permission Denied",
            "Packet sniffing requires administrator or root privileges.\n"
            "Please run this application with elevated privileges."
        )
    except Exception as e:
        log_text.insert(tk.END, f"Sniffing error: {e}\n")
        log_text.see(tk.END)
        messagebox.showerror("Sniffing Error", f"An error occurred while sniffing: {e}")
    finally:
        is_sniffing = False
        stop_sniffing_flag = False
        log_text.insert(tk.END, "Packet sniffing stopped.\n")
        log_text.see(tk.END)
        update_button_states(sniffing=False)


def start_sniffing():
    """
    Start the packet sniffing process based on user input.
    """
    global sniffing_thread, packet_filter, stop_sniffing_flag, captured_packets
    
    # Reset flags and clear captured packets
    stop_sniffing_flag = False
    captured_packets.clear()
    log_text.delete(1.0, tk.END)
    
    # Get filter type
    filter_type = filter_var.get()
    if filter_type == "TCP":
        packet_filter = "tcp"
    elif filter_type == "UDP":
        packet_filter = "udp"
    elif filter_type == "ICMP":
        packet_filter = "icmp"
    else:
        packet_filter = ""
    
    # Log start message
    filter_display = filter_type if filter_type != "All" else "all protocols"
    log_text.insert(tk.END, f"Starting packet capture ({filter_display})...\n")
    log_text.see(tk.END)
    
    # Start sniffing in a separate daemon thread
    sniffing_thread = threading.Thread(target=sniff_packets, daemon=True)
    sniffing_thread.start()


def stop_sniffing():
    """
    Stop the packet sniffing process.
    """
    global stop_sniffing_flag
    
    if is_sniffing:
        stop_sniffing_flag = True
        log_text.insert(tk.END, "Stopping packet capture...\n")
        log_text.see(tk.END)
        root.after(500, update_button_states)


def save_to_pcap_and_text():
    """
    Save captured packets to a PCAP file and packet summaries to a text file.
    """
    global captured_packets
    
    if not captured_packets:
        messagebox.showwarning("No Packets", "No packets have been captured yet.")
        return
    
    # Ask the user for a base filename
    filename = filedialog.asksaveasfilename(
        defaultextension=".pcap",
        filetypes=[("PCAP files", "*.pcap"), ("All files", "*.*")]
    )
    if not filename:
        return
    
    # Save to PCAP file
    try:
        wrpcap(filename, captured_packets)
        log_text.insert(tk.END, f"Saved {len(captured_packets)} packets to {filename}\n")
        log_text.see(tk.END)
        messagebox.showinfo("Success", f"Saved {len(captured_packets)} packets to PCAP file.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save PCAP file: {e}")
        return
    
    # Save to text file
    text_filename = filename.rsplit(".", 1)[0] + ".txt"
    try:
        with open(text_filename, "w", encoding="utf-8") as text_file:
            for packet in captured_packets:
                text_file.write(f"{packet.summary()}\n")
        log_text.insert(tk.END, f"Saved packet summaries to {text_filename}\n")
        log_text.see(tk.END)
        messagebox.showinfo("Success", f"Packet summaries saved to text file.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save text file: {e}")


def clear_log():
    """
    Clear the packet log and reset captured packets.
    """
    global captured_packets
    
    log_text.delete(1.0, tk.END)
    captured_packets.clear()
    log_text.insert(tk.END, "Packet log cleared.\n")
    log_text.see(tk.END)


def update_button_states(sniffing=False):
    """
    Update button states based on sniffing status.
    
    Args:
        sniffing: Boolean indicating if currently sniffing.
    """
    if sniffing:
        start_button.config(state="disabled")
        stop_button.config(state="normal")
        filter_frame.config(state="disabled")
        limit_entry.config(state="disabled")
    else:
        start_button.config(state="normal")
        stop_button.config(state="disabled")
        filter_frame.config(state="normal")
        limit_entry.config(state="normal")


def on_closing():
    """
    Handle window closing event.
    """
    global stop_sniffing_flag
    
    if is_sniffing:
        stop_sniffing_flag = True
        if sniffing_thread and sniffing_thread.is_alive():
            sniffing_thread.join(timeout=2)
    
    root.destroy()


# Create the main GUI window
root = tk.Tk()
root.title("Enhanced Packet Sniffer")
root.geometry("700x600")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Frame for filter options
filter_frame = tk.LabelFrame(root, text="Filter Options", padx=10, pady=10)
filter_frame.pack(padx=10, pady=10, fill="x")

filter_var = tk.StringVar(value="All")
tk.Radiobutton(filter_frame, text="All Packets", variable=filter_var, value="All").pack(anchor="w")
tk.Radiobutton(filter_frame, text="TCP Packets", variable=filter_var, value="TCP").pack(anchor="w")
tk.Radiobutton(filter_frame, text="UDP Packets", variable=filter_var, value="UDP").pack(anchor="w")
tk.Radiobutton(filter_frame, text="ICMP Packets", variable=filter_var, value="ICMP").pack(anchor="w")

# Frame for packet limit
limit_frame = tk.LabelFrame(root, text="Packet Limit (0 = unlimited)", padx=10, pady=10)
limit_frame.pack(padx=10, pady=10, fill="x")

limit_entry = tk.Entry(limit_frame)
limit_entry.pack(fill="x")
limit_entry.insert(0, "0")

# Frame for log output
log_frame = tk.LabelFrame(root, text="Packet Log", padx=10, pady=10)
log_frame.pack(padx=10, pady=10, fill="both", expand=True)

log_text = tk.Text(log_frame, wrap=tk.WORD, height=15)
log_text.pack(fill="both", expand=True, side="left")

# Add scrollbar to log
scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
scrollbar.pack(side="right", fill="y")
log_text.config(yscrollcommand=scrollbar.set)

# Frame for buttons
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack(fill="x")

start_button = tk.Button(button_frame, text="Start Sniffing", command=start_sniffing, bg="green", fg="white")
start_button.pack(side="left", padx=5)

stop_button = tk.Button(button_frame, text="Stop Sniffing", command=stop_sniffing, bg="red", fg="white", state="disabled")
stop_button.pack(side="left", padx=5)

save_button = tk.Button(button_frame, text="Save Packets", command=save_to_pcap_and_text, bg="blue", fg="white")
save_button.pack(side="left", padx=5)

clear_button = tk.Button(button_frame, text="Clear Log", command=clear_log, bg="orange", fg="white")
clear_button.pack(side="left", padx=5)

# Initial button state
update_button_states(sniffing=False)

# Start the GUI event loop
if __name__ == "__main__":
    root.mainloop()
