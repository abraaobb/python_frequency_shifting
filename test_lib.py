import numpy as np
import sounddevice as sd

fs = 44100
duration = 2  # segundos
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
tone = 0.5 * np.sin(2 * np.pi * 440 * t)  # tom 440Hz

sd.play(tone, fs)
sd.wait()
