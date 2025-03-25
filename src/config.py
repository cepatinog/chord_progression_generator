import os
from pathlib import Path

# Rutas globales
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data2'
MIDI_DIR = DATA_DIR / 'midi'
WAV_DIR = DATA_DIR / 'wav'
JAMS_DIR = DATA_DIR / 'jams'

# Ajustes de audio, BPM, etc.
DEFAULT_TEMPO = 60
DEFAULT_SAMPLE_RATE = 16000
