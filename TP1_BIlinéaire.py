# TP complet : lecture .wav, ajout bruit (3 sinusoides), FIR (Kaiser) et IIR (Butter/Cheb),
# affichages (temps, TFD en dB, h[n], H(f)), filtrage et comparaison.
import numpy as np
import scipy.signal as sp
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import sounddevice as sd

# ---------- Fonctions utilitaires ----------
def compute_TFD_db(x, fe, nfft=65536):
    """Retourne (f, X_db) pour la FFT centrée (en Hz, dB)."""
    N_fft = int(nfft)
    X = np.fft.fft(x, n=N_fft)
    X = np.fft.fftshift(X)
    mag = np.abs(X)
    mag_db = 20 * np.log10(np.maximum(mag, 1e-12))
    f = np.linspace(-fe/2, fe/2, N_fft, endpoint=False)
    return f, mag_db

def plot_TFD_db_subplot(ax, f, Xdb, positive_only=True, label=None):
    """Trace la TFD en dB en affichant la partie positive si demandée."""
    if positive_only:
        mid = len(f)//2
        ax.plot(f[mid:], Xdb[mid:], label=label)
        ax.set_xlim(0, f.max()/2)
    else:
        ax.plot(f, Xdb, label=label)
    ax.set_xlabel('Fréquence (Hz)')
    ax.set_ylabel('Amplitude (dB)')
    ax.grid(True)

def play_audio_safe(x, fe):
    """Joue x en normalisant correctement pour sounddevice."""
    x_play = np.array(x, dtype=float)
    m = np.max(np.abs(x_play))
    if m > 0:
        x_play = x_play / m * 0.95  # normalise à [-0.95, 0.95]
    sd.play(x_play, fe)
    sd.wait()

def zplane_silent(b, a=1):
    """Retourne zeros, poles (silencieux)."""
    zeros = np.roots(b)
    poles = np.roots(a)
    return zeros, poles

# ---------- Lecture du fichier ----------
fe, x = wav.read('vousavezducourrierenattente.wav')  
if x.ndim > 1:
    x = np.mean(x, axis=1)
x = x.astype(float)
N = len(x)
Te = 1.0/fe
t = np.arange(N) * Te

# ---------- Affichage signal temporel ----------
# plt.figure(figsize=(10,4))
# plt.plot(t, x)
# plt.title("Signal original - domaine temporel")
# plt.xlabel("Temps (s)")
# plt.ylabel("Amplitude")
# plt.grid(True)
# plt.tight_layout()

# ---------- TFD du signal original (en dB) ----------
f_orig, Xdb_orig = compute_TFD_db(x, fe)
#plt.figure(figsize=(10,4))
ax = plt.gca()
#plot_TFD_db_subplot(ax, f_orig, Xdb_orig, positive_only=True)
#plt.title("TFD du signal original (dB)")
#plt.tight_layout()

# ---------- Ajouter du bruit : 3 sinusoides ----------

Amax = 0.4 * np.max(np.abs(x)) 
amps = [Amax, 0.8*Amax, 0.6*Amax]
freqs = [1500.0, 2000.0, 3000.0]
bruit = np.zeros_like(x)
for A, f0 in zip(amps, freqs):
    bruit += A * np.cos(2*np.pi*f0*t)
Xb = x + bruit
play_audio_safe(Xb, fe)

# ---------- TFD du signal bruité ----------
f_b, Xdb_b = compute_TFD_db(Xb, fe)
#plt.figure(figsize=(10,4))
ax = plt.gca()
plot_TFD_db_subplot(ax, f_b, Xdb_b)
# plt.title("TFD du signal bruité (dB)")
# plt.tight_layout()

# ---------- Conception FIR (Kaiser window) ----------
Aa_req = 55.0            
Deltaf_max = fe / 10.0    
fc = 1200.0             
Deltaf = min(400.0, Deltaf_max)

nyq = fe / 2.0
width = Deltaf / nyq  # largeur normalisée (0..1)
N_kaiser, beta = sp.kaiserord(Aa_req, width)
# Assurer numtaps >= 3
if N_kaiser < 3:
    N_kaiser = 3
# firwin demande numtaps (N) ; typiquement N_kaiser odd est meilleur pour linéar phase symétrique
if N_kaiser % 2 == 0:
    N_kaiser += 1

print("FIR Kaiser: numtaps =", N_kaiser, ", beta =", beta, ", fc =", fc, "Hz, Deltaf =", Deltaf, "Hz")
b_fir = sp.firwin(numtaps=N_kaiser, cutoff=fc, window=('kaiser', beta), fs=fe)
a_fir = np.array([1.0])

# Réponse impulsionnelle et fréquence du FIR
h_fir = b_fir
w_fir, H_fir = sp.freqz(b_fir, a_fir, worN=8192, fs=fe)
Hf_db = 20*np.log10(np.maximum(np.abs(H_fir), 1e-12))

# plt.figure(figsize=(10,6))
# plt.subplot(2,1,1)
# plt.stem(np.arange(len(h_fir))/fe, h_fir, basefmt=" ")
# plt.xlabel("Temps (s)")
# plt.ylabel("h[n]")
# plt.title("Réponse impulsionnelle du FIR (Kaiser)")
# plt.grid(True)

# plt.subplot(2,1,2)
# plt.plot(w_fir, Hf_db)
# plt.xlabel("Fréquence (Hz)")
# plt.ylabel("Amplitude (dB)")
# plt.title("Réponse en fréquence du FIR (dB)")
# plt.grid(True)
# plt.tight_layout()

# Filtrage du signal bruité avec FIR
y_fir = sp.lfilter(b_fir, a_fir, Xb)

# TFD du signal filtré (FIR)
f_yfir, Ydb_fir = compute_TFD_db(y_fir, fe)
# plt.figure(figsize=(10,4))
#plot_TFD_db_subplot(plt.gca(), f_yfir, Ydb_fir)
# plt.title("TFD du signal filtré (FIR) en dB")
# plt.tight_layout()

# ---------- Conception IIR (bilinear) : Butterworth, Cheby1, Cheby2 ----------
Ap = 2.0      
Aa = 50.0     

wp = fc
ws = fc + Deltaf
Wp = wp / nyq 
Ws = ws / nyq

designs = {}
for prot in ['butter', 'cheby1', 'cheby2']:
    if prot == 'butter':
        N_iir, Wn = sp.buttord(Wp, Ws, Ap, Aa)
        b_iir, a_iir = sp.butter(N_iir, Wn, btype='low', analog=False, output='ba')
    elif prot == 'cheby1':
        N_iir, Wn = sp.cheb1ord(Wp, Ws, Ap, Aa)
        b_iir, a_iir = sp.cheby1(N_iir, rp=Ap, Wn=Wn, btype='low', analog=False, output='ba')
    elif prot == 'cheby2':
        N_iir, Wn = sp.cheb2ord(Wp, Ws, Ap, Aa)
        b_iir, a_iir = sp.cheby2(N_iir, rs=Aa, Wn=Wn, btype='low', analog=False, output='ba')

    print(f"{prot}: ordre = {N_iir}, Wn(normalized) = {Wn}")
    designs[prot] = (b_iir, a_iir, N_iir)

# Pour chaque IIR : réponses et filtrage
for prot, (b_iir, a_iir, N_iir) in designs.items():
    # Impulsionnel discret
    imp_len = 200
    tout, h_iir = sp.dimpulse((b_iir, a_iir, 1.0/fe), n=imp_len)
    h_iir = np.squeeze(h_iir)

    # Réponse en fréquence
    w_iir, H_iir = sp.freqz(b_iir, a_iir, worN=8192, fs=fe)
    H_iir_db = 20*np.log10(np.maximum(np.abs(H_iir), 1e-12))

    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.plot(np.arange(len(h_iir))/fe, h_iir)
    plt.xlabel("Temps (s)")
    plt.ylabel("h[n]")
    plt.title(f"Réponse impulsionnelle - {prot} (N={N_iir})")
    plt.grid(True)

    plt.subplot(1,2,2)
    plt.plot(w_iir, H_iir_db)
    plt.xlabel("Fréquence (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.title(f"Réponse en fréquence - {prot}")
    plt.grid(True)
    plt.tight_layout()

    # Filtrage
    y_iir = sp.lfilter(b_iir, a_iir, Xb)

    # TFD du filtré
    f_yiir, Ydb_iir = compute_TFD_db(y_iir, fe)
    plt.figure(figsize=(8,4))
    ax = plt.gca()
    plot_TFD_db_subplot(ax, f_orig, Xdb_orig, label='Original')
    plot_TFD_db_subplot(ax, f_b, Xdb_b, label='Bruitée')
    plot_TFD_db_subplot(ax, f_yiir, Ydb_iir, label=f'Filtrée ({prot})')
    plt.title(f'Comparaison TFD: original - bruitée - filtrée ({prot})')
    plt.legend()
    plt.tight_layout()

    play_audio_safe(y_iir, fe)

print("\n--- Résumé et conseils ---")
print(f"FIR Kaiser : numtaps = {N_kaiser}, beta = {beta}, fc = {fc} Hz, Deltaf = {Deltaf} Hz")
for prot, (b_iir, a_iir, N_iir) in designs.items():
    ftest = min(int(1.5*fc), int(nyq-1))
    _, H_test = sp.freqz(b_iir, a_iir, worN=[2*np.pi*ftest/fe], fs=fe)
    att = 20*np.log10(np.maximum(np.abs(H_test[0]), 1e-12))
    print(f"{prot}: ordre {N_iir}, atténuation approximative à {ftest} Hz = {att:.1f} dB")

print("""
Interprétation :
- Le filtre FIR (Kaiser) est linéaire en phase => préserve la forme temporelle de la parole, mais peut demander un ordre élevé (beaucoup de coefficients).
- Les filtres IIR (Butterworth, Chebyshev) atteignent la même atténuation avec un ordre plus faible (moins de calcul), mais ont une phase non-linéaire (peut déformer la forme temporelle).
- Butterworth : réponse en amplitude la plus "lisse" (monotone) mais pas d'ondulation.
- Cheby1 : ripple dans la bande passante (meilleure pente), Cheby2 : ripple dans la bande d'arrêt.
=> Si préserver la qualité temporelle de la parole est important -> choisir FIR. Si contraintes de complexité/temps réel -> IIR (Butterworth si tu veux pas de ripple).
""")

plt.show()
