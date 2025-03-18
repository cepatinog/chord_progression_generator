# JazzNet Chord Generation

Este repositorio contiene un pipeline para generar, convertir y anotar progresiones de acordes en formato MIDI, WAV y JAMS.

## 🚀 Instalación

1. Clona este repositorio:
   ```sh
   git clone https://github.com/TU-USUARIO/jazznet-chord-generation.git
   cd jazznet-chord-generation

2. Crea y activa un entorno virtual:

    ```sh
    conda create --name jazznet-env python=3.9
    conda activate jazznet-env

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt

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

1. **Python 3.9** o superior (dependiendo de compatibilidad).
2. Librerías indicadas en `requirements.txt`:
   - `midiutil`
   - `jams<...` (asegurarse de usar NumPy < 2.0 para evitar conflictos)
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
- Define rutas globales (BASE_DIR, DATA_DIR, MIDI_DIR, WAV_DIR, JAMS_DIR) y parámetros como `DEFAULT_TEMPO` y `DEFAULT_SAMPLE_RATE`.

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
- Mapea numerales romanos (ej: `"ii,7"`, `"V,7"`) a etiquetas que cumple el **regex** de JAMS (ej: `"D:min7"`, `"G:7"`).
- Maneja un **key** (p. ej. `"C"`) y asume tonalidades mayores simplificadas.

### 3.5. `jams_creation.py`
- Crea `.jams` para cada `.mid` en una carpeta, usando la función anterior para obtener la etiqueta `"D:min7"` en `Annotation.value`.
- Almacena los numerales romanos en `annotation.sandbox.roman_numerals` y la tonalidad en `annotation.sandbox.key`.

---

## 4. Uso en el Notebook

En `notebooks/chord_progressions.ipynb` se demuestra el **pipeline**:

1. **Generar** `.mid` con `generate_progression(...)`, por ejemplo:
   ```python
   from src.generate_progression import generate_progression
   generate_progression("ii,7-V,7-I,maj7", "ii7-V7-Imaj7_demo")

2. **Convertir** a `.wav`:

    ```python
    from src.audio_conversion import convert_all_mid_in_folder
    midi_folder = Path("data/midi/ii7-V7-Imaj7_demo")
    convert_all_mid_in_folder(midi_folder)

2. **Crear**  `.jams`:
    
    ```python
    from src.jams_creation import create_jams_for_folder
    roman_seq = ["ii,7", "V,7", "I,maj7"]
    key = "C"
    create_jams_for_folder(midi_folder, roman_seq, key, "ii7-V7-Imaj7_C")


4. **Revisar** la carpeta data/ para ver los .mid, .wav y .jams generados.


5. **Sugerencias de Extensión**:
Manejar bemoles (Db, Eb) en roman_to_chord.py.
Soportar tonalidades menores y más sufijos (por ej. dim7, sus4, hdim7).


6. **Créditos y Licencia**
Proyecto inspirado en la lógica JazzNet para la generación de acordes masiva y la anotación en .jams.
Las dependencias principales son midiutil, timidity y jams.

