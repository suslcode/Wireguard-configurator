import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import subprocess
import qrcode
import os

def generate_keys():
    private_key = subprocess.getoutput("wg genkey")
    public_key = subprocess.getoutput(f"echo {private_key} | wg pubkey")
    return private_key, public_key

def generate_preshared_key():
    return subprocess.getoutput("wg genpsk")

def on_generate_private_key():
    private_key, _ = generate_keys()
    client_private_key_entry.delete(0, tk.END)
    client_private_key_entry.insert(0, private_key)

def on_generate_preshared_key():
    preshared_key = generate_preshared_key()
    client_preshared_key_entry.delete(0, tk.END)
    client_preshared_key_entry.insert(0, preshared_key)

def create_conf_file():
    filename = simpledialog.askstring("Input", "Enter the filename:")
    if filename:
        with open(f"{filename}.conf", "w") as file:
            file.write("[Interface]\n")
            file.write(f"PrivateKey = {client_private_key_entry.get()}\n")
            file.write(f"Address = {client_address_entry.get()}\n")
            file.write(f"ListenPort = {client_listen_port_entry.get()}\n")
            file.write(f"DNS = {client_dns_entry.get()}\n\n")
            file.write("[Peer]\n")
            file.write(f"PublicKey = {server_public_key_entry.get()}\n")
            file.write(f"PresharedKey = {client_preshared_key_entry.get()}\n")
            file.write(f"Endpoint = {endpoint_entry.get()}\n")
            file.write(f"AllowedIPs = {allowed_ips_entry.get()}\n")
        messagebox.showinfo("Info", "Configuration file created successfully!")

def create_qr_code():
    filepath = filedialog.askopenfilename(title="Select the conf file", filetypes=[("Configuration files", "*.conf")])
    if not filepath:
        return

    with open(filepath, 'r') as file:
        data = file.read()

    img = qrcode.make(data)
    img.save(filepath + ".png")

app = tk.Tk()
app.title("WireGuard Client Configurator")

interface_frame = ttk.LabelFrame(app, text="Interface", padding=(10, 5))
interface_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

client_private_key_label = ttk.Label(interface_frame, text="Private Key:")
client_private_key_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
client_private_key_entry = ttk.Entry(interface_frame, width=50)
client_private_key_entry.grid(row=0, column=1, padx=5, pady=5)
client_private_key_button = ttk.Button(interface_frame, text="Generate", command=on_generate_private_key)
client_private_key_button.grid(row=0, column=2, padx=5, pady=5)

client_address_label = ttk.Label(interface_frame, text="Address:")
client_address_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
client_address_entry = ttk.Entry(interface_frame, width=50)
client_address_entry.grid(row=1, column=1, padx=5, pady=5)

client_listen_port_label = ttk.Label(interface_frame, text="ListenPort:")
client_listen_port_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
client_listen_port_entry = ttk.Entry(interface_frame, width=50)
client_listen_port_entry.grid(row=2, column=1, padx=5, pady=5)

client_dns_label = ttk.Label(interface_frame, text="DNS:")
client_dns_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
client_dns_entry = ttk.Entry(interface_frame, width=50)
client_dns_entry.grid(row=3, column=1, padx=5, pady=5)

peer_frame = ttk.LabelFrame(app, text="Peer", padding=(10, 5))
peer_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

server_public_key_label = ttk.Label(peer_frame, text="Server Public Key:")
server_public_key_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
server_public_key_entry = ttk.Entry(peer_frame, width=50)
server_public_key_entry.grid(row=0, column=1, padx=5, pady=5)

client_preshared_key_label = ttk.Label(peer_frame, text="PresharedKey:")
client_preshared_key_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
client_preshared_key_entry = ttk.Entry(peer_frame, width=50)
client_preshared_key_entry.grid(row=1, column=1, padx=5, pady=5)
client_preshared_key_button = ttk.Button(peer_frame, text="Generate", command=on_generate_preshared_key)
client_preshared_key_button.grid(row=1, column=2, padx=5, pady=5)

endpoint_label = ttk.Label(peer_frame, text="Endpoint:")
endpoint_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
endpoint_entry = ttk.Entry(peer_frame, width=50)
endpoint_entry.grid(row=2, column=1, padx=5, pady=5)

allowed_ips_label = ttk.Label(peer_frame, text="AllowedIPs:")
allowed_ips_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
allowed_ips_entry = ttk.Entry(peer_frame, width=50)
allowed_ips_entry.grid(row=3, column=1, padx=5, pady=5)

create_conf_button = ttk.Button(app, text="Create conf", command=create_conf_file)
create_conf_button.grid(row=2, column=0, pady=10)

create_qr_button = ttk.Button(app, text="Create QR-code", command=create_qr_code)
create_qr_button.grid(row=3, column=0, pady=10)

app.mainloop()
