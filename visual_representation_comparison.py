import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, spectrogram

def deslocar_frequencia(sinal, fs, deslocamento_hz, metodo="hilbert"):
    t = np.arange(len(sinal)) / fs
    omega = 2 * np.pi * deslocamento_hz

    if metodo == "cos":
        portadora = np.cos(omega * t)
        resultado = sinal * portadora

    elif metodo == "exp":
        portadora = np.exp(1j * omega * t)
        resultado = np.real(sinal * portadora)

    elif metodo == "hilbert":
        sinal_analitico = hilbert(sinal)
        portadora = np.exp(1j * omega * t)
        resultado = np.real(sinal_analitico * portadora)

    else:
        raise ValueError("Método inválido. Use: 'cos', 'exp' ou 'hilbert'.")

    return resultado

def plotar_espectrograma(sinal, fs, titulo, subplot_idx, total_plots):
    plt.subplot(2, 2, subplot_idx)
    f, t_spec, Sxx = spectrogram(sinal, fs, nperseg=512, noverlap=256)
    plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx + 1e-12), shading='gouraud')
    plt.title(titulo)
    plt.ylabel("Frequência (Hz)")
    plt.xlabel("Tempo (s)")
    plt.colorbar(label='dB')

def comparar_deslocamentos(sinal_original, fs, deslocamento_hz):
    metodos = ["cos", "exp", "hilbert"]
    plt.figure(figsize=(14, 8))

    # Original
    plotar_espectrograma(sinal_original, fs, "Original", 1, 4)

    # Deslocamentos
    for idx, metodo in enumerate(metodos, start=2):
        sinal_mod = deslocar_frequencia(sinal_original, fs, deslocamento_hz, metodo)
        plotar_espectrograma(
            sinal_mod,
            fs,
            f"{metodo.upper()} ({'+' if deslocamento_hz >= 0 else ''}{deslocamento_hz} Hz)",
            idx,
            4
        )

    plt.tight_layout()
    plt.show()

# Sinal original: 1500 Hz
fs = 8000
t = np.linspace(0, 2, 2 * fs, endpoint=False)
sinal = np.sin(2 * np.pi * 1500 * t)

# Deslocar de 1500 Hz para 500 Hz → deslocamento -1000 Hz
comparar_deslocamentos(sinal, fs, deslocamento_hz=-1000)
