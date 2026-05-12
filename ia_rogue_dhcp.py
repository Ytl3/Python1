from scapy.all import *
import time
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# ==================== CONFIGURATION ====================
IFACE = "VMware Network Adapter VMnet1"
# Chemins (à adapter si besoin)
DOSSIER_PROJET = "C:/Users/DELL/Desktop/Projet_Rogue_DHCP"
CSV_PATH = os.path.join(DOSSIER_PROJET, "dhcp_dataset.csv")
MODELE_PATH = os.path.join(DOSSIER_PROJET, "rogue_dhcp_model.pkl")
# Identifiants pour le blocage (comme dans l'ancien code)
USER = "Administrator"
PASSWORD = "Admin123"
# =======================================================

# --- 1. Charger ou entraîner le modèle IA (Random Forest) ---
if not os.path.exists(MODELE_PATH):
    print("Entraînement du modèle...")
    df = pd.read_csv(CSV_PATH, sep=';')
    X = df.drop('label', axis=1)
    y = df['label']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODELE_PATH)
    print("Modèle entraîné et sauvegardé.")
else:
    model = joblib.load(MODELE_PATH)

# --- 2. Fonction de blocage (reprise de l'ancien code qui marche) ---
def bloquer_rogue(ip, user=USER, password=PASSWORD):
    """
    Bloque le serveur DHCP non autorisé sur la machine cible.
    Utilise schtasks pour arrêter et désactiver le service DHCPServer.
    """
    create = f'schtasks /create /s {ip} /u {user} /p {password} /tn "StopRogue" /tr "cmd /c net stop DHCPServer && sc config DHCPServer start= disabled" /sc once /st 00:00 /ru SYSTEM /f'
    run = f'schtasks /run /s {ip} /u {user} /p {password} /tn "StopRogue"'
    delete = f'schtasks /delete /s {ip} /u {user} /p {password} /tn "StopRogue" /f'
    subprocess.run(create, shell=True, capture_output=True)
    subprocess.run(run, shell=True, capture_output=True)
    subprocess.run(delete, shell=True, capture_output=True)
    print(f"Rogue {ip} bloqué (service DHCPServer arrêté/désactivé)")
    return True

# --- 3. Interface Tkinter et variables globales ---
serveurs = {}
rogues_deja_bloques = set()
tree = None
text_log = None

def log(message):
    timestamp = time.strftime("%H:%M:%S")
    text_log.insert(tk.END, f"[{timestamp}] {message}\n")
    text_log.see(tk.END)

def mettre_a_jour_tableau(ip, mac, statut, nb_offres):
    for row in tree.get_children():
        if tree.item(row)['values'][0] == ip:
            tree.item(row, values=(ip, mac, statut, nb_offres))
            return
    if statut == "ROGUE":
        tree.insert('', tk.END, values=(ip, mac, statut, nb_offres), tags=('rogue',))
    else:
        tree.insert('', tk.END, values=(ip, mac, statut, nb_offres), tags=('legitime',))

def extraire_features_pour_modele(packet):
    """Extrait les 10 features numériques utilisées par Random Forest."""
    options = {opt[0]: opt[1] for opt in packet[DHCP].options if isinstance(opt, tuple)}
    ip_src = packet[IP].src
    return [[
        1 if 'subnet_mask' in options else 0,
        1 if 'router' in options else 0,
        1 if 'name_server' in options else 0,
        1 if 'domain' in options else 0,
        1 if 'broadcast_address' in options else 0,
        1 if 'server_id' in options else 0,
        options.get('lease_time', 0),
        len(options),
        int(ip_src.split('.')[-1]),
        int(options.get('server_id', '0.0.0.0').split('.')[-1]) if 'server_id' in options else 0,
    ]]

def analyser_paquet(packet):
    if DHCP in packet and packet[DHCP].options[0][1] == 2:
        ip_src = packet[IP].src
        mac_src = packet[Ether].src
        features = extraire_features_pour_modele(packet)
        prediction = model.predict(features)[0]

        if ip_src not in serveurs:
            serveurs[ip_src] = {'mac': mac_src, 'nb_offres': 1}
        else:
            serveurs[ip_src]['nb_offres'] += 1

        if prediction == 1:
            log(f"*** ALERTE : Rogue détecté {ip_src} ({mac_src}) ***")
            mettre_a_jour_tableau(ip_src, mac_src, "ROGUE", serveurs[ip_src]['nb_offres'])
            bloquer_rogue(ip_src, USER, PASSWORD)
        else:
            log(f"Légitime : {ip_src} ({mac_src})")
            mettre_a_jour_tableau(ip_src, mac_src, "Légitime", serveurs[ip_src]['nb_offres'])
            
def boucle_detection():
    log("Démarrage de la détection IA (Random Forest) avec blocage automatique...")
    sniff(iface=IFACE, filter="udp and (port 67 or port 68)", prn=analyser_paquet, store=0)

# --- 4. Lancement de l'interface ---
root = tk.Tk()
root.title("Détecteur Rogue DHCP - IA + Blocage")
root.geometry("900x600")
root.configure(bg='#1e1e1e')

titre = tk.Label(root, text="🤖 Détecteur Rogue DHCP avec Intelligence Artificielle", font=("Arial", 14, "bold"), bg='#1e1e1e', fg='white')
titre.pack(pady=10)

frame_table = tk.Frame(root, bg='#1e1e1e')
frame_table.pack(fill=tk.BOTH, expand=True, padx=10)

columns = ('IP', 'MAC', 'Statut', 'Nb Offres')
tree = ttk.Treeview(frame_table, columns=columns, show='headings', height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)
tree.tag_configure('rogue', background='#ff4444', foreground='white')
tree.tag_configure('legitime', background='#44ff44', foreground='black')
tree.pack(fill=tk.BOTH, expand=True)

log_label = tk.Label(root, text="Logs :", bg='#1e1e1e', fg='white', font=("Arial", 10))
log_label.pack(anchor='w', padx=10)

text_log = scrolledtext.ScrolledText(root, height=12, bg='#2d2d2d', fg='#00ff00', font=("Courier", 9))
text_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

thread = threading.Thread(target=boucle_detection, daemon=True)
thread.start()

root.mainloop()