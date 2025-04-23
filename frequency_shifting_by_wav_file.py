import os
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt


def deslocar_frequencia(input_wav, output_wav, deslocamento_frequencia):
    # Verificar se o arquivo de entrada existe
    if not os.path.exists(input_wav):
        print(f"Erro: O arquivo {input_wav} não foi encontrado.")
        return

    # Carregar o arquivo WAV
    taxa_amostragem, dados = wav.read(input_wav)

    # Verificar se o áudio é estéreo ou mono
    if len(dados.shape) > 1:
        print("O áudio possui mais de um canal (estéreo). Usando apenas o primeiro canal.")
        dados = dados[:, 0]  # Considerar apenas o canal esquerdo para simplificar

    # Verificar se o áudio está vazio
    if len(dados) == 0:
        print("Erro: O arquivo de áudio está vazio.")
        return

    # Informações sobre os dados de entrada
    print(f"Taxa de Amostragem: {taxa_amostragem} Hz")
    print(f"Número Total de Amostras: {len(dados)}")
    print(f"Amplitude Máxima do Original: {np.max(dados)}")

    # Normalizar os dados do áudio para o intervalo [-1, 1]
    dados = dados / np.max(np.abs(dados))

    # Aplicar a transformação no domínio do tempo diretamente com exponenciais complexas
    n = np.arange(len(dados))
    dados_deslocados = dados * np.exp(2j * np.pi * deslocamento_frequencia * n / taxa_amostragem)

    # Retornar ao formato real
    dados_deslocados = np.real(dados_deslocados)

    # Normalizar para o formato int16
    dados_deslocados = np.int16(dados_deslocados / np.max(np.abs(dados_deslocados)) * 32767)

    # Salvar o novo arquivo WAV
    wav.write(output_wav, taxa_amostragem, dados_deslocados)
    print(f"Arquivo deslocado salvo em: {output_wav}")

    # Visualizações
    plt.figure(figsize=(14, 10))

    # *** Gráfico 1: Forma de Onda do Áudio Original ***
    plt.subplot(4, 1, 1)
    tempo_original = np.linspace(0, len(dados) / taxa_amostragem, num=len(dados))
    plt.plot(tempo_original, dados, color='blue')
    plt.title('Forma de Onda - Áudio Original')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid()

    # *** Gráfico 2: Forma de Onda do Áudio Deslocado ***
    plt.subplot(4, 1, 2)
    tempo_deslocado = np.linspace(0, len(dados_deslocados) / taxa_amostragem, num=len(dados_deslocados))
    plt.plot(tempo_deslocado, dados_deslocados, color='orange')
    plt.title('Forma de Onda - Áudio com Frequência Deslocada')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid()

    # *** Gráfico 3: Espectrograma do Áudio Original ***
    plt.subplot(4, 1, 3)
    plt.specgram(dados, Fs=taxa_amostragem, NFFT=2048, noverlap=1024, cmap='viridis')
    plt.title('Espectrograma - Áudio Original')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequência (Hz)')
    plt.colorbar(label='Intensidade (dB)')

    # *** Gráfico 4: Espectrograma do Áudio Deslocado ***
    plt.subplot(4, 1, 4)
    plt.specgram(dados_deslocados, Fs=taxa_amostragem, NFFT=2048, noverlap=1024, cmap='magma')
    plt.title('Espectrograma - Áudio com Frequência Deslocada')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequência (Hz)')
    plt.colorbar(label='Intensidade (dB)')

    # Ajustes Finais
    plt.tight_layout()
    plt.show()


# Exemplo de uso
input_wav = 'downloads/original_ytd.wav'  # Caminho do arquivo de entrada
output_wav = 'downloads/saida_deslocada_v1.wav'  # Caminho do arquivo de saída
deslocamento_frequencia = 2000
deslocar_frequencia(input_wav, output_wav, deslocamento_frequencia)
