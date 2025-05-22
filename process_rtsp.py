import subprocess
import numpy as np
import sounddevice as sd
from scipy.signal import hilbert
import queue
import threading
import time

sample_rate = 44100
channels = 1
chunk_size = 8192  # bloco maior para processar
shift_hz = 400

ffmpeg_cmd = [
    'ffmpeg',
    '-i', 'rtsp://localhost:8554/audio',
    '-f', 's16le',
    '-acodec', 'pcm_s16le',
    '-ac', str(channels),
    '-ar', str(sample_rate),
    '-'
]

proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

audio_queue = queue.Queue(maxsize=20)  # buffer entre leitura e áudio

def frequency_shift_hilbert(x, sample_rate, shift_hz):
    analytic_signal = hilbert(x)
    t = np.arange(len(x)) / sample_rate
    shifted = np.real(analytic_signal * np.exp(2j * np.pi * shift_hz * t))
    return shifted.astype(np.float32)

def reader_thread():
    """Lê dados do ffmpeg e coloca na fila"""
    while True:
        raw_data = proc.stdout.read(chunk_size * 2)
        if len(raw_data) < chunk_size * 2:
            break
        audio_data = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
        audio_queue.put(audio_data)

def callback(outdata, frames, time, status):
    try:
        data = audio_queue.get(timeout=1)  # espera dados no buffer
        shifted = frequency_shift_hilbert(data, sample_rate, shift_hz)
        outdata[:len(shifted), 0] = shifted
        if len(shifted) < frames:
            outdata[len(shifted):] = 0
    except queue.Empty:
        outdata.fill(0)  # silêncio se não tem dados

# Inicia thread de leitura
thread = threading.Thread(target=reader_thread, daemon=True)
thread.start()

with sd.OutputStream(samplerate=sample_rate, channels=channels, blocksize=chunk_size, callback=callback):
    print(f"Tocando áudio deslocado em frequência ({shift_hz}Hz) com buffer. Ctrl+C para parar.")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

proc.terminate()
