import numpy as np
import soundfile as sf
from scipy.signal import hilbert
import matplotlib.pyplot as plt

def deslocar_frequencia(input_wav, output_wav, deslocamento_hz):
    # Carrega o áudio
    y, sr = sf.read(input_wav)

    # Garante que é mono (1 canal)
    if y.ndim > 1:
        y = y.mean(axis=1)

    # Gera sinal analítico (domínio complexo)
    y_analytic = hilbert(y)

    # Vetor de tempo
    t = np.arange(len(y)) / sr

    # Modulação para deslocar a frequência
    y_shifted = y_analytic * np.exp(2j * np.pi * deslocamento_hz * t)

    # Parte real do sinal deslocado
    y_result = np.real(y_shifted)

    # Normaliza para o intervalo [-1, 1]
    y_result = y_result / np.max(np.abs(y_result))

    # Salva o arquivo resultante
    sf.write(output_wav, y_result, sr)
    print(f"✅ Áudio salvo em: {output_wav}")

    # Plotagem dos gráficos
    plt.figure(figsize=(14, 10))

    # Forma de onda original
    plt.subplot(4, 1, 1)
    tempo = np.linspace(0, len(y) / sr, num=len(y))
    plt.plot(tempo, y, color='blue')
    plt.title('Forma de Onda - Áudio Original')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid()

    # Forma de onda deslocada
    plt.subplot(4, 1, 2)
    plt.plot(tempo, y_result, color='orange')
    plt.title('Forma de Onda - Áudio com Frequência Deslocada')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid()

    # Espectrograma original
    plt.subplot(4, 1, 3)
    plt.specgram(y, Fs=sr, NFFT=2048, noverlap=1024, cmap='viridis')
    plt.title('Espectrograma - Áudio Original')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequência (Hz)')
    plt.colorbar(label='Intensidade (dB)')

    # Espectrograma deslocado
    plt.subplot(4, 1, 4)
    plt.specgram(y_result, Fs=sr, NFFT=2048, noverlap=1024, cmap='magma')
    plt.title('Espectrograma - Áudio com Frequência Deslocada')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequência (Hz)')
    plt.colorbar(label='Intensidade (dB)')

    plt.tight_layout()
    plt.show()

# Exemplo de uso
deslocar_frequencia("downloads/original_ytd.wav", "downloads/saida_deslocada_v2_visual.wav", deslocamento_hz=2000)
