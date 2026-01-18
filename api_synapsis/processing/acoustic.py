import parselmouth
from parselmouth.praat import call
import numpy as np
import matplotlib.pyplot as plt
import os

def analizar_audio(path_audio, output_dir):
    snd = parselmouth.Sound(path_audio)

    # ===== PITCH =====
    pitch = snd.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    pitch_values = pitch_values[pitch_values > 0]
    times = pitch.xs()[:len(pitch_values)]

    f0_mean = np.mean(pitch_values)
    f0_min = np.min(pitch_values)
    f0_max = np.max(pitch_values)

    # ===== IMAGEN PITCH =====
    pitch_img = os.path.join(output_dir, "pitch.png")
    plt.figure(figsize=(6, 3))
    plt.plot(times, pitch_values)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("F0 (Hz)")
    plt.title("Pitch")
    plt.tight_layout()
    plt.savefig(pitch_img)
    plt.close()

    # ===== ESPECTROGRAMA =====
    spectrogram = snd.to_spectrogram()
    spec_img = os.path.join(output_dir, "spectrogram.png")

    plt.figure(figsize=(6, 3))
    plt.imshow(
        spectrogram.values,
        origin="lower",
        aspect="auto",
        extent=[
            spectrogram.xmin,
            spectrogram.xmax,
            spectrogram.ymin,
            spectrogram.ymax,
        ]
    )
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Frecuencia (Hz)")
    plt.title("Espectrograma")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(spec_img)
    plt.close()

    # ===== JITTER / SHIMMER =====
    point_process = call(snd, "To PointProcess (periodic, cc)", 75, 500)
    try:
        jitter = call(point_process, "Get jitter (local)", 0, 0, 75, 500, 1.3)
        shimmer = call([snd, point_process], "Get shimmer (local)", 0, 0, 75, 500, 1.3)
    except:
        jitter = 0.0
        shimmer = 0.0

    # ===== TABLA PITCH =====
    pitch_table = [
        {"time": float(t), "f0": float(f)}
        for t, f in zip(times[:50], pitch_values[:50])
    ]

    return {
        "F0_mean": float(f0_mean),
        "F0_min": float(f0_min),
        "F0_max": float(f0_max),
        "jitter": float(jitter),
        "shimmer": float(shimmer),
        "pitch_image": pitch_img,
        "spectrogram_image": spec_img,
        "pitch_table": pitch_table
    }
