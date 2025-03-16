NOTE_ARRAY = ["C", "C#", "D", "Eb", "E", "F",
              "F#", "G", "Ab", "A", "Bb", "B"]

def roman_to_midi(base_midi, numeral):
    """
    Convierte un numeral romano como 'I', 'ii', 'V' a notas MIDI 
    basándose en la lógica de JazzNet.
    """
    # Ejemplo simplificado
    # ...
    return [base_midi, base_midi+4, base_midi+7]

def create_progression(base_midi, progression):
    """
    Dada una lista de numerales romanos, crea una lista de acordes en MIDI.
    """
    chords = []
    for numeral in progression:
        chord = roman_to_midi(base_midi, numeral)
        chords.append(chord)
    return chords
