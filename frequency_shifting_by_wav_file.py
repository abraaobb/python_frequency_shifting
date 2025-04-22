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

    # Informações sobre os dados de saída
    print(f"Amplitude Máxima do Áudio Deslocado: {np.max(dados_deslocados)}")

    # ** Gráficos para Visualização **
    plt.figure(figsize=(12, 6))

    # Áudio Original
    plt.subplot(2, 1, 1)
    plt.plot(dados[:min(1000, len(dados))], label="Áudio Original", color='blue')
    plt.title('Áudio Original')
    plt.xlabel('Amostras')
    plt.ylabel('Amplitude')
    plt.legend()

    # Áudio Deslocado
    plt.subplot(2, 1, 2)
    plt.plot(dados_deslocados[:min(1000, len(dados_deslocados))], label="Áudio Deslocado", color='orange')
    plt.title('Áudio com Frequência Deslocada')
    plt.xlabel('Amostras')
    plt.ylabel('Amplitude')
    plt.legend()

    # Mostrar gráficos
    plt.tight_layout()
    plt.show()


# Exemplo de uso
input_wav = 'downloads/original_ytd.wav'  # Caminho do arquivo de entrada
output_wav = 'downloads/saida_deslocada.wav'  # Caminho do arquivo de saída
deslocamento_frequencia = 500  # Deslocamento em Hz

deslocar_frequencia(input_wav, output_wav, deslocamento_frequencia)
