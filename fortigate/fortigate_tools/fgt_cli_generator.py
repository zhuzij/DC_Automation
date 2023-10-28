########################################
# Fortinet Debug Tool
# Author Raymond Troche
# Tool designed to create script output
# Debugging and Traige firewall issues
# Version 1.0
# 10-25-2023
########################################
 
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import font

# Function to toggle port entry widget state based on the checkbox state
def toggle_port_entry_state():
    if ping_checkbox_var.get() == 1:
        # source_port_entry.config(state="disabled")
        dest_port_entry.config(state="disabled")
        tcp_checkbox.config(state="disabled")
        udp_checkbox.config(state="disabled")
    else:
        # source_port_entry.config(state="normal")
        dest_port_entry.config(state="normal")
        tcp_checkbox.config(state="normal")
        udp_checkbox.config(state="normal")
 
# Function to generate Debug Flow-Verify Traffic commands with custom filters
def generate_debug_flow_commands(reverse_var):
    # source_port = source_port_entry.get().strip()
    dest_port = dest_port_entry.get().strip()
    source_ip = source_ip_entry.get().strip()
    dest_ip = dest_ip_entry.get().strip()
    is_ping_checked = ping_checkbox_var.get()
 
    # check the state of reverse_var. If reverse_var.get() == 1, then swap the source and destination fields before generating the command.
    if reverse_var.get() == 1:
        source_ip, dest_ip = dest_ip, source_ip
        # source_port, dest_port = dest_port, source_port

    # Initialize the command
    debug_flow_command = ''
    # debug_flow_command = "Debug Flow-Verify Traffic\n"
    debug_flow_command += "diagnose debug enable\n"
 
    # Generate filters based on non-empty input fields
    filters = []
    if is_ping_checked:
        # If PING is checked, use protocol 1 for ICMP
        filters.append(f"proto 1")
    if source_ip:
        filters.append(f"saddr {source_ip}: source address")
    if dest_ip:
        filters.append(f"daddr {dest_ip}: destination address")
    # if source_port:
    #     filters.append(f"sport {source_port}: source port")
    if not is_ping_checked:
        if dest_port:
            filters.append(f"dport {dest_port}: destination port")
 
    # Add filters to the command if there are any
    for filter_str in filters:
        # Remove the ":" and the text after it in the filter descriptions
        filter_str = filter_str.split(':')[0]
        debug_flow_command += f"diagnose debug flow filter {filter_str}\n"
 
    debug_flow_command += "diagnose debug flow show function-name enable\n"
    debug_flow_command += "diagnose debug flow trace start 100\n"
 
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, debug_flow_command)
 
# Function to generate Sniffer commands based on input values
def generate_sniffer_commands(reverse_var):
    source_ip = source_ip_entry.get().strip()
    dest_ip = dest_ip_entry.get().strip()  # Corrected the typo here
    # source_port = source_port_entry.get().strip()
    dest_port = dest_port_entry.get().strip()
    tcp_checked = tcp_checkbox_var.get()
    udp_checked = udp_checkbox_var.get()
    is_ping_checked = ping_checkbox_var.get()
    
    # check the state of reverse_var. If reverse_var.get() == 1, then swap the source and destination fields before generating the command.
    if reverse_var.get() == 1:
        source_ip, dest_ip = dest_ip, source_ip
        # source_port, dest_port = dest_port, source_port

    # Initialize the command for the sniffer
    sniffer_command = ''
    # sniffer_command = "Diagnose Sniffer-Verify Flow\n"
    sniffer_filter = []

    
    if source_ip:
        sniffer_filter.append(f"host {source_ip}")
    if dest_ip:
        sniffer_filter.append(f"host {dest_ip}")
    if is_ping_checked:
        sniffer_filter.append("icmp")
    else:
        if dest_port:
            if tcp_checked:
                sniffer_filter.append(f"tcp port {dest_port}")
            if udp_checked:
                sniffer_filter.append(f"udp port {dest_port}")
 
    if sniffer_filter:
        sniffer_command += f"diagnose sniffer packet any '{' and '.join(sniffer_filter)}' 4\n"
 
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, sniffer_command)
 
# Function to generate IPROPE commands based on input values
def generate_iprope_commands(reverse_var):
    source_ip = source_ip_entry.get().strip()
    dest_ip = dest_ip_entry.get().strip()
    # source_port = 0 if ping_checkbox_var.get() else source_port_entry.get().strip()
    source_port = 1024
    dest_port = 0 if ping_checkbox_var.get() else dest_port_entry.get().strip()
    is_ping_checked = ping_checkbox_var.get()
    interface = interface_entry.get().strip()
 
    # check the state of reverse_var. If reverse_var.get() == 1, then swap the source and destination fields before generating the command.
    if reverse_var.get() == 1:
        source_ip, dest_ip = dest_ip, source_ip
        # source_port, dest_port = dest_port, source_port

    # Determine the protocol based on TCP, UDP, or PING
    if is_ping_checked:
        protocol = "1/"  # ICMP
        source_port = 0
    else:
        if tcp_checkbox_var.get():
            protocol = "6"  # TCP
        elif udp_checkbox_var.get():
            protocol = "17"  # UDP
        else:
            protocol = "0"  # Not specified
 
    # Initialize the IPROPE command
    iprope_command = f"diagnose firewall iprope lookup {source_ip} {source_port} {dest_ip} {dest_port} {protocol} {interface}\n"
 
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, iprope_command)

def on_reverse_checkbox_toggle():
    if reverse_var.get() == 1:
        messagebox.showwarning("Change Interface", "Please be aware to get Interface changed to the correct ingress interface name now at the reverse traffic direction.")

def on_ping_checkbox_toggle():
    if ping_checkbox_var.get() == 1:
        messagebox.showinfo("Note", "For more accurate policy lookup results, please use the Policy Lookup Tool within the Fortigate Admin Portal instead.")

# Function to copy text from the text widget to clipboard
def copy_cli_to_clipboard():
    cli_text = result_text.get("1.0", "end-1c")  # Assuming cli_text_widget is the name of your Text widget
    app.clipboard_clear()
    app.clipboard_append(cli_text)
    app.update()  # Update the clipboard

# Create the main application window
app = tk.Tk()
app.title("FortiGate Command Generator - Debug Flow-Verify Traffic, Sniffer, and IPROPE")
 
# Create input fields and labels for the filters
filter_frame = tk.Frame(app)
filter_frame.pack()
 
# Add a checkbox for PING
ping_checkbox_var = tk.IntVar()
ping_checkbox = tk.Checkbutton(filter_frame, text="PING", variable=ping_checkbox_var, 
                               command=lambda: [toggle_port_entry_state(), on_ping_checkbox_toggle()])
ping_checkbox.grid(row=3, column=2)
 
# Create input fields and labels for the filters
# source_port_label = tk.Label(filter_frame, text="Source Port:")
# source_port_label.grid(row=0, column=1)
# source_port_entry = tk.Entry(filter_frame)
# source_port_entry.grid(row=0, column=2)
 
dest_port_label = tk.Label(filter_frame, text="Destination Port:")
dest_port_label.grid(row=2, column=1)
dest_port_entry = tk.Entry(filter_frame)
dest_port_entry.grid(row=2, column=2)
 
tcp_checkbox_var = tk.IntVar()
tcp_checkbox = tk.Checkbutton(filter_frame, text="TCP", variable=tcp_checkbox_var)
tcp_checkbox.grid(row=3, column=3)
udp_checkbox_var = tk.IntVar()
udp_checkbox = tk.Checkbutton(filter_frame, text="UDP", variable=udp_checkbox_var)
udp_checkbox.grid(row=3, column=4)
 
source_ip_label = tk.Label(filter_frame, text="Source IP:")
source_ip_label.grid(row=1, column=1)
source_ip_entry = tk.Entry(filter_frame)
source_ip_entry.grid(row=1, column=2)
 
dest_ip_label = tk.Label(filter_frame, text="Destination IP:")
dest_ip_label.grid(row=1, column=3)
dest_ip_entry = tk.Entry(filter_frame)
dest_ip_entry.grid(row=1, column=4)
 
# Add an input field for the Interface
interface_label = tk.Label(filter_frame, text="Interface:")
interface_label.grid(row=2, column=3)
interface_entry = tk.Entry(filter_frame)
interface_entry.grid(row=2, column=4)
 
# Add Checkbox for "Reverse Traffic Direction" and prompt user to input new ingress interface name
reverse_var = tk.IntVar()
reverse_checkbox = tk.Checkbutton(app, text='Reverse Traffic Direction', variable=reverse_var, command=on_reverse_checkbox_toggle)
reverse_checkbox.pack()

# Button to generate Debug Flow-Verify Traffic commands
generate_debug_flow_button = tk.Button(app, text="Generate Debug Flow-Verify Traffic Commands", command=lambda: generate_debug_flow_commands(reverse_var))
generate_debug_flow_button.pack()
 
# Button to generate Sniffer commands
generate_sniffer_button = tk.Button(app, text="Generate Sniffer Commands", command=lambda: generate_sniffer_commands(reverse_var))
generate_sniffer_button.pack()
 
# Button to generate IPROPE commands
generate_iprope_button = tk.Button(app, text="Generate IPROPE Commands", command=lambda: generate_iprope_commands(reverse_var))
generate_iprope_button.pack()
 
# Text area to display generated commands with a wider width
result_text = tk.Text(app, height=15, width=80)  # Increased width to accommodate long lines

# Add "Copy CLI" button
copy_cli_button = tk.Button(app, text="Copy CLI", command=copy_cli_to_clipboard)
copy_cli_button.pack()
result_text.pack()
 
app.mainloop()