#!/usr/bin/env python

from midiutil import MIDIFile
from pathlib import Path
from .config import MIDI_DIR

# Listas y arreglos originales de JazzNet
NOTE_ARRAY = ["C", "C#", "D", "Eb", "E", "F",
              "F#", "G", "Ab", "A", "Bb", "B"]
OCTAVE_ARRAY = [1, 2, 3, 4, 5, 6, 7, 8]
ALTERATIONS_ARR = ["7", "7b5", "7#5", "maj7", "maj7b5", "maj7#5"]

def baseChords(firstNote, numeral):
    """
    Dado un numeral romano (I, i, etc.) retorna tres notas (note1, note2, note3)
    que forman la triada correspondiente (mayor si es mayúscula, menor si es minúscula).
    Cada nota está representada como un valor MIDI.
    """
    # Triada base: mayor o menor
    if numeral.isupper():
        note1 = firstNote
        note2 = note1 + 4
        note3 = note2 + 3
    else:  # numeral.islower()
        note1 = firstNote
        note2 = note1 + 3
        note3 = note2 + 4
    return note1, note2, note3

def raiseNote(note1, note2, note3, raiseVal):
    """
    Aplica sostenido (#) o bemol (b) a las tres notas de una triada.
    Devuelve la triada modificada.
    """
    if raiseVal == "#":
        return note1 + 1, note2 + 1, note3 + 1
    elif raiseVal == "b":
        return note1 - 1, note2 - 1, note3 - 1

def chordAlteration(note1, note2, note3, ext):
    """
    Dado un acorde triada y una extensión (7, maj7, 7#5, etc.),
    genera un acorde de cuatro notas (tetrad).
    """
    if ext == "7":
        note4 = note3 + 3
    elif ext == "7b5":
        note3 -= 1
        note4 = note3 + 4
    elif ext == "7#5":
        note3 += 1
        note4 = note3 + 4
    elif ext == "maj7":
        note4 = note3 + 4
    elif ext == "maj7b5":
        note3 -= 1
        note4 = note3 + 4
    elif ext == "maj7#5":
        note3 += 1
        note4 = note3 + 4
    return note1, note2, note3, note4

def chordInversions3(note1, note2, note3, inv):
    """
    Aplica la inversión (0, 1 o 2) a un acorde triada.
    - inv=0 -> sin inversión
    - inv=1 -> primera inversión (nota1 sube 12 semitonos)
    - inv=2 -> segunda inversión (nota1 y nota2 suben 12 semitonos)
    """
    if inv == 1:
        note1 += 12
    elif inv == 2:
        note1 += 12
        note2 += 12
    return note1, note2, note3

def chordInversions4(note1, note2, note3, note4, inv):
    """
    Aplica la inversión (0, 1, 2 o 3) a un acorde tetrad.
    - inv=0 -> sin inversión
    - inv=1 -> primera inversión (nota1 sube 12 semitonos)
    - inv=2 -> segunda inversión (nota1, nota2 suben 12)
    - inv=3 -> tercera inversión (nota1, nota2, nota3 suben 12)
    """
    if inv == 1:
        note1 += 12
    elif inv == 2:
        note1 += 12
        note2 += 12
    elif inv == 3:
        note1 += 12
        note2 += 12
        note3 += 12
    return note1, note2, note3, note4

def generate_progression(progression: str, name: str, output_dir=MIDI_DIR, tempo=60):
    """
    Genera archivos .mid para la progresión dada (3 o 4 acordes).
    Explora todas las notas en NOTE_ARRAY, octavas en OCTAVE_ARRAY y
    todas las inversiones posibles.
    
    :param progression: str, e.g. "ii-V-I" or "ii,#,7-V-I"
    :param name: str, nombre corto para etiquetar los archivos generados (carpeta y prefijo)
    :param output_dir: str, carpeta base donde se guardarán los .mid
    :param tempo: int, BPM para los archivos MIDI
    """

    # Separar la progresión en acordes (p.ej. ["ii", "V", "I"] o ["ii,#,7", "V", "I"])
    progChords = progression.split("-")
    if len(progChords) not in [3, 4]:
        raise ValueError("Only 3- or 4-chord progressions are supported.")

    # Directorio de salida
    output_path = Path(output_dir) / name
    output_path.mkdir(parents=True, exist_ok=True)

    # Combinamos cada nota + octava, generando algo como "C-1", "C#-1", ... "B-8".
    nameArray = []
    for o in OCTAVE_ARRAY:
        for n in NOTE_ARRAY:
            noteName = f"{n}-{o}"
            nameArray.append(noteName)

    # Recorremos nameArray con un índice MIDI (24..108)
    for idx, noteName in enumerate(nameArray):
        base_midi = 24 + idx  # 24 => C1, 108 => B7 (aprox)
        chordArr = []

        # 1. Procesar cada acorde de la progresión
        for numeral in progChords:
            numeralArr = numeral.split(',')
            # Determinamos la nota base según el numeral romano
            if numeralArr[0] in ["I", "i"]:
                firstNote = base_midi
            elif numeralArr[0] in ["II", "ii"]:
                firstNote = base_midi + 2
            elif numeralArr[0] in ["III", "iii"]:
                firstNote = base_midi + 4
            elif numeralArr[0] in ["IV", "iv"]:
                firstNote = base_midi + 5
            elif numeralArr[0] in ["V", "v"]:
                firstNote = base_midi + 7
            elif numeralArr[0] in ["VI", "vi"]:
                firstNote = base_midi + 9
            elif numeralArr[0] in ["VII", "vii"]:
                firstNote = base_midi + 11
            else:
                raise ValueError(f"Unrecognized chord numeral: {numeralArr[0]}")

            # Generar la triada base
            note1, note2, note3 = baseChords(firstNote, numeralArr[0])
            chord = (note1, note2, note3)

            # Manejo de alteraciones / extensiones
            if len(numeralArr) > 1:
                token = numeralArr[1]
                if token in ["#", "b"]:
                    note1, note2, note3 = raiseNote(note1, note2, note3, token)
                    chord = (note1, note2, note3)

                    # Si existe una tercera parte => ext (p.ej. '7')
                    if len(numeralArr) == 3 and numeralArr[2] in ALTERATIONS_ARR:
                        note1, note2, note3, note4 = chordAlteration(note1, note2, note3, numeralArr[2])
                        chord = (note1, note2, note3, note4)
                elif token in ALTERATIONS_ARR:
                    # Tetrad directa
                    note1, note2, note3, note4 = chordAlteration(note1, note2, note3, token)
                    chord = (note1, note2, note3, note4)
                else:
                    raise ValueError("Unrecognized token after comma.")

            chordArr.append(chord)

        # 2. Una vez definimos chordArr, generamos .mid con cada inversión
        track = 0
        channel = 0
        duration = 2
        volume = 100

        if len(chordArr) == 3:
            # 3 acordes
            tempArr1, tempArr2, tempArr3 = chordArr
            num = 0
            for c1 in range(len(tempArr1)):
                for c2 in range(len(tempArr2)):
                    for c3 in range(len(tempArr3)):
                        MyMIDI = MIDIFile(1)
                        MyMIDI.addTempo(track, 0, tempo)
                        timeOffset = 0

                        # Acorde 1
                        if len(tempArr1) == 3:
                            inv1 = chordInversions3(*tempArr1, c1)
                        else:
                            inv1 = chordInversions4(*tempArr1, c1)
                        for note in inv1:
                            MyMIDI.addNote(track, channel, note, timeOffset, duration, volume)
                        timeOffset += 2

                        # Acorde 2
                        if len(tempArr2) == 3:
                            inv2 = chordInversions3(*tempArr2, c2)
                        else:
                            inv2 = chordInversions4(*tempArr2, c2)
                        for note in inv2:
                            MyMIDI.addNote(track, channel, note, timeOffset, duration, volume)
                        timeOffset += 2

                        # Acorde 3
                        if len(tempArr3) == 3:
                            inv3 = chordInversions3(*tempArr3, c3)
                        else:
                            inv3 = chordInversions4(*tempArr3, c3)
                        for note in inv3:
                            MyMIDI.addNote(track, channel, note, timeOffset, duration, volume)
                        timeOffset += 2

                        # Guardar .mid
                        filename = f"{noteName}-{name}-{num}.mid"
                        filepath = output_path / filename
                        with open(filepath, "wb") as outmidi:
                            MyMIDI.writeFile(outmidi)
                        num += 1

        elif len(chordArr) == 4:
            # 4 acordes
            tempArr1, tempArr2, tempArr3, tempArr4 = chordArr
            num = 0
            for c1 in range(len(tempArr1)):
                for c2 in range(len(tempArr2)):
                    for c3 in range(len(tempArr3)):
                        for c4 in range(len(tempArr4)):
                            MyMIDI = MIDIFile(1)
                            MyMIDI.addTempo(track, 0, tempo)
                            timeOffset = 0

                            # Acorde 1
                            if len(tempArr1) == 3:
                                inv1 = chordInversions3(*tempArr1, c1)
                            else:
                                inv1 = chordInversions4(*tempArr1, c1)
                            for note in inv1:
                                MyMIDI.addNote(track, channel, note, timeOffset, duration, volume)
                            timeOffset += 2

                            # Acorde 2
                            if len(tempArr2) == 3:
                                inv2 = chordInversions3(*tempArr2, c2)
                            else:
                                inv2 = chordInversions4(*tempArr2, c2)
                            for note in inv2:
                                MyMIDI.addNote(track, channel, note, timeOffset, duration, volume)
                            timeOffset += 2

                            # Acorde 3
                            if len(tempArr3) == 3:
                                inv3 = chordInversions3(*tempArr3, c3)
                            else:
                                inv3 = chordInversions4(*tempArr3, c3)
                            for note in inv3:
                                MyMIDI.addNote(track, channel, note, timeOffset, duration, volume)
                            timeOffset += 2

                            # Acorde 4
                            if len(tempArr4) == 3:
                                inv4 = chordInversions3(*tempArr4, c4)
                            else:
                                inv4 = chordInversions4(*tempArr4, c4)
                            for note in inv4:
                                MyMIDI.addNote(track, channel, note, timeOffset, duration, volume)
                            timeOffset += 2

                            # Guardar .mid
                            filename = f"{noteName}-{name}-{num}.mid"
                            filepath = output_path / filename
                            with open(filepath, "wb") as outmidi:
                                MyMIDI.writeFile(outmidi)
                            num += 1

    print(f"Generated progression '{progression}' -> folder: {output_path}")

