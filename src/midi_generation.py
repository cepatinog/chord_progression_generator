from midiutil import MIDIFile
from .config import MIDI_DIR, DEFAULT_TEMPO

def create_midi(chords, filename, bpm=DEFAULT_TEMPO):
    """
    Genera un archivo MIDI con una secuencia de acordes.
    :param chords: lista de listas, donde cada sublista contiene notas MIDI de un acorde
    :param filename: nombre del archivo .mid
    :param bpm: tempo en BPM
    :return: ruta del archivo .mid generado
    """
    midi = MIDIFile(1)
    track = 0
    time = 0
    volume = 100

    midi.addTempo(track, time, bpm)

    # Cada acorde dura 2 beats, por ejemplo
    for chord in chords:
        for note in chord:
            midi.addNote(track, 0, note, time, 2, volume)
        time += 2

    filepath = MIDI_DIR / filename
    MIDI_DIR.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as f:
        midi.writeFile(f)
    return filepath
