# JazzNet Chord Generation

Este repositorio contiene un pipeline para generar, convertir y anotar progresiones de acordes en formato MIDI, WAV y JAMS.


## 🚀 Instalación

1. Clona este repositorio:

   ```sh
   git clone https://github.com/TU-USUARIO/jazznet-chord-generation.git
   cd jazznet-chord-generation
   ```

2. Crea y activa un entorno virtual:

   ```sh
   conda create --name jazznet-env python=3.9
   conda activate jazznet-env
   ```

3. Instala las dependencias:

   ```sh
   pip install -r requirements.txt
   ```

---


## 📂 Estructura del Proyecto

```
CHORD_PROGRESSION_GENERATOR/
│
├── data/
│   ├── midi/   # Archivos .mid que se generan
│   ├── wav/        # Archivos .wav convertidos
│   └── jams/       # Archivos .jams con anotaciones
│
├── notebooks/
│   └── chord_progressions.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuración global (rutas de carpetas, etc.)
│   ├── generate_progression.py  # Funciones principales basadas en jazznet
│   ├── audio_conversion.py # Funciones para convertir MIDI a WAV, etc.
│   ├── jams_creation.py    # Funciones para generar JAMS
│   ├── roman_to_chord.py      # Lógica de notación en números romanos y conversion a regex de JAMS
│
├── main.py                 # Punto de entrada si quisiéramos un CLI
├── requirements.txt
├── README.md
└── .gitignore

```

---

## 2. Requisitos y Dependencias

1. **Python 3.9** o superior.
2. Librerías indicadas en `requirements.txt`:
   - `midiutil`
   - `jams`
   - `numpy<2.0`
   - `jsonschema`
   - etc.
3. **Timidity** instalado a nivel de sistema:
   - Ubuntu/Debian:
     ```bash
     sudo apt-get update
     sudo apt-get install timidity
     ```
   - macOS (Homebrew):
     ```bash
     brew install timidity
     ```
   - Windows: Instalar Timidity++ y asegurarse de que el ejecutable `timidity` esté en el `PATH`.

---

## 3. Módulos Principales

### 3.1. `config.py`

- Define rutas globales (BASE\_DIR, DATA\_DIR, MIDI\_DIR, WAV\_DIR, JAMS\_DIR) y parámetros como `DEFAULT_TEMPO` y `DEFAULT_SAMPLE_RATE`.

### 3.2. `generate_progression.py`

- Genera `.mid` en **todas las tonalidades** (C1..B7) y **todas las inversiones** para una progresión de **3 o 4 acordes**.
- Usa notación con comas para separar la base y la extensión en cada acorde:
  - Ejemplo: `"ii,7-V,7-I,maj7"` en lugar de `"ii7-V7-Imaj7"`.
- Guarda los `.mid` en `data/midi/<nombre_de_progresion>`.

### 3.3. `audio_conversion.py`

- Convierte cada archivo `.mid` a `.wav` usando **Timidity**, creando la misma estructura de subcarpetas en `data/wav`.
- Funciones:
  - `midi_to_wav(midi_file)`: convierte un archivo puntual.
  - `convert_all_mid_in_folder(folder)`: convierte todos los `.mid` dentro de una carpeta.

### 3.4. `roman_to_chord.py`

- Mapea numerales romanos (ej: `"ii,7"`, `"V,7"`) a etiquetas que cumplen el **regex** de JAMS (ej: `"D:min7"`, `"G:7"`).
- Extrae la tónica real de cada `.mid` generado en cualquier tonalidad.
- Maneja tonalidades mayores y menores.

### 3.5. `jams_creation.py`

- Crea `.jams` para cada `.mid` en una carpeta, asegurando que se usa la tonalidad correcta detectada.
- Los numerales romanos originales quedan en `annotation.sandbox.roman_numerals`.
- La tonalidad detectada queda en `annotation.sandbox.key`.

---

## 4. Uso en el Notebook

En `notebooks/chord_progressions.ipynb` se demuestra el **pipeline**:

1. **Generar** `.mid` con `generate_progression(...)`, por ejemplo:

   ```python
   from src.generate_progression import generate_progression
   generate_progression("ii,7-V,7-I,maj7", "ii7-V7-Imaj7")
   ```

2. **Convertir** a `.wav`:

   ```python
   from src.audio_conversion import convert_all_mid_in_folder
   from pathlib import Path
   midi_folder = Path("data/midi/ii7-V7-Imaj7")
   convert_all_mid_in_folder(midi_folder)
   ```

3. **Crear** `.jams` con tonalidad extraída del `.mid`:

   ```python
   from src.jams_creation import create_jams_for_folder
   create_jams_for_folder(midi_folder)
   ```

4. **Revisar** la carpeta `data/` para ver los `.mid`, `.wav` y `.jams` generados.

---

## 5. Consideraciones y Mejoras Futuras

- **Soporte para Escalas y Modos**: Ampliar `roman_to_chord.py` para admitir más tipos de escalas.
- **Detección Automática de Tónica**: Mejorar la extracción de tonalidad desde los `.mid`.

---

## Créditos y Licencia

Este proyecto se basa en la lógica de JazzNet para la generación masiva de progresiones de acordes y su anotación en `.jams`. Usa `midiutil`, `timidity`, `jams` y otras bibliotecas.


