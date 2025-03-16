import subprocess
from pathlib import Path
from .config import WAV_DIR

def midi_to_wav(midi_path, wav_name):
    """
    Convierte un archivo MIDI a WAV usando Timidity o Fluidsynth.
    """
    WAV_DIR.mkdir(parents=True, exist_ok=True)
    output_wav = WAV_DIR / wav_name

    # Ejemplo con timidity
    subprocess.call([
        'timidity',
        str(midi_path),
        '-Ow1',
        '-s', '16k',
        '-o', str(output_wav)
    ])
    return output_wav
