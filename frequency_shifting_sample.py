# Reexecutando o código após o reset do estado

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import hilbert

# Parâmetros do sinal
fs = 44100  # frequência de amostragem
duration = 5.0  # duração em segundos
f_signal = 5000  # frequência original
f_shift = -4500  # deslocamento desejado (rebaixar em 4500 Hz)

# Geração do tempo
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Sinal original real (seno de 5 kHz)
signal_real = np.sin(2 * np.pi * f_signal * t)

# Obter a versão analítica do sinal (sinal complexo)
analytic_signal = hilbert(signal_real)

# Deslocamento de frequência (multiplicação por exponencial complexa)
shifted_signal_complex = analytic_signal * np.exp(1j * 2 * np.pi * f_shift * t)

# Obter a parte real do sinal deslocado (sinal utilizável)
shifted_signal_real = np.real(shifted_signal_complex)

# Normalização e salvamento do áudio
normalized_shifted = np.int16(shifted_signal_real / np.max(np.abs(shifted_signal_real)) * 32767)
write("downloads/sinal_deslocado.wav", fs, normalized_shifted)

# Plotando os sinais
plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.title("Sinal Original (5 kHz)")
plt.plot(t[:1000], signal_real[:1000])
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.title("Sinal Deslocado (5 kHz → 500 Hz)")
plt.plot(t[:1000], shifted_signal_real[:1000])
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()
