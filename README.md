# Proyecto-de-Estudio-Parkison
Proyecto de estudio para detección temprana de Parkinson

# Módulo de Análisis Acústico – SYNAPSIS

## 1. Descripción
Este proyecto corresponde al módulo de análisis acústico automático del sistema SYNAPSIS, orientado al estudio de parámetros vocales relevantes para la detección y seguimiento del Parkinson.

El sistema permite cargar audios de voz, analizarlos utilizando Praat-Parselmouth y generar métricas acústicas y visualizaciones que luego pueden ser integradas a un sistema clínico mayor.

---

## 2. Objetivo del Proyecto
Desarrollar un entorno local que:
- Analice audios de voz automáticamente
- Extraiga parámetros acústicos (Pitch, F0, etc.)
- Genere gráficos (Pitch y Espectrograma)
- Organice los resultados por paciente
- Permita futura integración con PHP y MySQL

---

## 3. Tecnologías Utilizadas
- Python 3.10+
- Flask
- Praat-Parselmouth
- NumPy
- Matplotlib
- HTML / CSS (Bootstrap)
- WAMP (para futura integración con MySQL)

---

## 4. explicación del codigo

# 1. Librerías Importadas

```python
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
```

## parselmouth

Interfaz de Python para el software de análisis fonético **Praat**.

Permite acceder desde Python a algoritmos acústicos usados en investigación de voz.

Ejemplos de parámetros que puede calcular:

- pitch (F0)
- jitter
- shimmer
- HNR
- formantes
- intensidad

Entidad relevante: **Praat**

Documentación oficial:

https://parselmouth.readthedocs.io/

---

## numpy

Biblioteca fundamental para cálculo científico en Python.

Se utiliza para realizar operaciones matemáticas sobre arrays.

Ejemplos:

```python
np.mean()
np.std()
np.max()
np.min()
```

Permite calcular estadísticas del pitch.

Documentación:

https://numpy.org/doc/

---

## matplotlib

Biblioteca utilizada para generar visualizaciones.

Permite crear:

- gráficos
- espectrogramas
- visualizaciones acústicas

Documentación:

https://matplotlib.org/stable/index.html

---

## Librerías auxiliares

| Librería | Función |
|--------|--------|
| os | Manejar rutas y archivos |
| json | Guardar historial de análisis |
| datetime | Registrar fecha del análisis |

---

# 2. Función Principal

```python
def analizar_audio(path_audio, paciente_dir, sexo):
```

Define una función que recibe:

| Parámetro | Función |
|--------|--------|
| path_audio | Ubicación del archivo WAV |
| paciente_dir | Carpeta del paciente |
| sexo | Usado para comparar F0 con valores normativos |

---

# 3. Carga del Audio

```python
snd = parselmouth.Sound(path_audio)
```

Convierte el archivo `.wav` en un objeto **Sound de Praat**.

Esto permite aplicar todos los algoritmos acústicos de análisis.

---

# 4. Cálculo de Pitch (F0)

```python
pitch = snd.to_pitch()
pitch_values = pitch.selected_array["frequency"]
pitch_values = pitch_values[pitch_values > 0]
```

Calcula la **frecuencia fundamental de la voz (F0)**.

### Qué es F0

F0 es la **frecuencia de vibración de las cuerdas vocales**.

Valores típicos:

| Sexo | Rango típico |
|----|----|
| Hombres | 85 – 180 Hz |
| Mujeres | 165 – 255 Hz |

Referencia científica:

Titze, I. (1994) *Principles of Voice Production*

https://www.ncbi.nlm.nih.gov/books/NBK10924/

---

# 5. Estadísticas del Pitch

```python
f0_mean = np.mean(pitch_values)
pitch_std = np.std(pitch_values)
pitch_range = np.max(pitch_values) - np.min(pitch_values)
cv_pitch = pitch_std / f0_mean
```

Calcula propiedades estadísticas del pitch.

### F0 Mean (Promedio del pitch).

### Pitch Std (Variabilidad del pitch).

### Pitch Range (Diferencia entre el pitch máximo y mínimo).

### CV Pitch (Coeficiente de variación):

```
CV = desviación estándar / media
```

Se utiliza para medir **inestabilidad vocal**. (Hablando de la relacion de Estadistica con el uso de la frecuencia media)

---

# 6. Intensidad

```python
intensity = snd.to_intensity()
intensidad_mean = np.mean(intensity.values)
```

Calcula la intensidad promedio en **decibelios (dB)**.

Valores típicos de voz conversacional:

```
60 – 70 dB
```

Referencia:

Stevens, K. N. *Acoustic Phonetics*

---

# 7. Jitter

```python
point_process = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)", 75, 500)

jitter = parselmouth.praat.call(
    point_process,
    "Get jitter (local)",
    0,0,0.0001,0.02,1.3
)
```

### Qué es Jitter

Variación **ciclo a ciclo del periodo de vibración vocal**.

Indica irregularidad de la voz.

Valores normales:

| Parámetro | Valor típico |
|------|------|
| Jitter local | < 1 % |

Referencia:

https://www.fon.hum.uva.nl/praat/manual/Voice_2__Jitter.html

---

# 8. Shimmer

```python
shimmer = parselmouth.praat.call(
    [snd, point_process],
    "Get shimmer (local)",
    0,0,0.0001,0.02,1.3,1.6
)
```

### Qué es Shimmer

Variación **ciclo a ciclo de la amplitud vocal**.

Valores normales aproximados:

| Parámetro | Rango |
|------|------|
| Shimmer local | < 3 – 4 % |

Referencia:

https://www.fon.hum.uva.nl/praat/manual/Voice_3__Shimmer.html

---

# 9. HNR (Harmonic to Noise Ratio)

```python
hnr = parselmouth.praat.call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
hnr_mean = parselmouth.praat.call(hnr, "Get mean", 0, 0)
```

HNR mide la **relación entre componentes armónicos y ruido en la voz**.

Valores típicos:

| HNR | Interpretación |
|----|----|
| > 20 dB | Voz saludable |
| 10 – 20 dB | Ligera disfonía |
| < 10 dB | Voz patológica |

Referencia:

https://www.fon.hum.uva.nl/praat/manual/Harmonicity.html

---

# 10. Score Heurístico

```python
score = 0
```

Se implementa un sistema simple de clasificación basado en reglas.

Condiciones evaluadas:

- jitter > 1 %
- shimmer > 4 %
- hnr < 20

Cada condición suma **1 punto**.

Clasificación:

| Score | Interpretación |
|----|----|
| 0 | Normal |
| 1 | Leve |
| 2 | Moderado |
| 3 | Severo |

Aclaracion: Es solo un indicador.

---

# 11. Comparación Normativa de F0

```python
if sexo == "M":
    rango_min = 85
    rango_max = 180
else:
    rango_min = 165
    rango_max = 255
```

Se compara el F0 calculado con rangos fisiológicos típicos.

Referencias:

- Titze (1994)
- Boersma & Weenink – Praat Manual

---

# 12. Gráfico de Pitch

```python
plt.plot(pitch_values)
plt.axhline(f0_mean)
```

Genera una visualización de:

- evolución temporal del pitch
- promedio de F0

Se guarda como:

```
pitch.png
```

---

# 13. Espectrograma

```python
plt.specgram(snd.values[0], Fs=snd.sampling_frequency)
```

Genera un **espectrograma**, representación estándar en análisis acústico.

| Eje | Significado |
|----|----|
| X | Tiempo |
| Y | Frecuencia |
| Color | Energía |

Referencia:

https://en.wikipedia.org/wiki/Spectrogram

---

# 14. Guardado del Historial

Archivo generado:

```
historial.json
```

Se almacenan:

- fecha
- F0
- jitter
- shimmer
- HNR
- score

Esto permite **seguimiento longitudinal del paciente**.

---

# 15. Valores Devueltos

La función retorna un diccionario con los siguientes parámetros:

```
F0_mean
Pitch_std
Pitch_range
CV_pitch
Intensidad
Jitter
Shimmer
HNR
Score
Clasificacion
```

Estos datos pueden ser utilizados por:

- Frontend
- Base de datos
- Informes clínicos
