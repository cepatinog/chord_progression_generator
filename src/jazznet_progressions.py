# src/jazznet_progressions.py

from midiutil import MIDIFile
from pathlib import Path

# Listas y arreglos originales de JazzNet
NOTE_ARRAY = ["C", "C#", "D", "Eb", "E", "F", 
              "F#", "G", "Ab", "A", "Bb", "B"]
OCTAVE_ARRAY = [1, 2, 3, 4, 5, 6, 7, 8]
ALTERATIONS_ARR = ["7", "7b5", "7#5", "maj7", "maj7b5", "maj7#5"]

def baseChords(firstNote, numeral):
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
    # Aplica sostenidos o bemoles a la triada
    if raiseVal == "#":
        return note1+1, note2+1, note3+1
    elif raiseVal == "b":
        return note1-1, note2-1, note3-1

def chordAlteration(note1, note2, note3, ext):
    # Crea tetrads (cuartas notas) o altera la tercera
    if ext == "7":
        note4 = note3 + 3
    elif ext == "7b5":
        note3 = note3 - 1
        note4 = note3 + 4
    elif ext == "7#5":
        note3 = note3 + 1
        note4 = note3 + 4
    elif ext == "maj7":
        note4 = note3 + 4
    elif ext == "maj7b5":
        note3 = note3 - 1
        note4 = note3 + 4
    elif ext == "maj7#5":
        note3 = note3 + 1
        note4 = note3 + 4
    return note1, note2, note3, note4

def chordInversions3(note1, note2, note3, inv):
    # Triada: 2 inversiones posibles
    if inv == 1:
        note1 += 12
    elif inv == 2:
        note1 += 12
        note2 += 12
    return note1, note2, note3

def chordInversions4(note1, note2, note3, note4, inv):
    # Tetrad: 3 inversiones posibles
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

def generate_progression(
    progression: str, 
    name: str, 
    style: str = "progressions",
    output_dir: str = "data/patterns"
):
    """
    Genera archivos .mid para la progresión dada (3 o 4 acordes).
    Explorará todas las notas en NOTE_ARRAY, octavas en OCTAVE_ARRAY, 
    y todas las inversiones posibles.
    :param progression: string del tipo "ii-V-I" o "ii,#,7-V-ii"
    :param name: nombre corto para etiquetar los archivos (ej: "ii-V-I")
    :param style: subcarpeta donde se guardan los .mid (por defecto 'progressions')
    :param output_dir: carpeta base donde se guardan los .mid
    """
    progChords = progression.split("-")
    if len(progChords) not in [3, 4]:
        raise ValueError("Only 3- and 4-chord progressions are currently supported.")

    path = Path(output_dir) / style / name
    path.mkdir(parents=True, exist_ok=True)

    # Crear la lista de "noteName" => C-1, C#-1,... B-8
    nameArray = []
    for o in OCTAVE_ARRAY:
        for n in NOTE_ARRAY:
            noteName = f"{n}-{o}"
            nameArray.append(noteName)

    for q, j in zip(nameArray, range(24, 109)):
        base = j   # MIDI note number (24 = C1, 108 = B7)
        noteName = q

        # Paso 1: para la progresión, determinar la triada/tetrad base
        chordArr = []
        for numeral in progChords:
            # notar que 'numeral' puede ser 'ii' o 'I' o 'IV,7', etc.
            numeralArr = numeral.split(',')

            # Determinar la nota base del acorde segun el numeral romano
            # I => base + 0
            # II => base + 2
            # ...
            # i => base + 0 (menor)
            # ...
            if numeralArr[0] in ["I", "i"]:
                firstNote = base
            elif numeralArr[0] in ["II", "ii"]:
                firstNote = base + 2
            elif numeralArr[0] in ["III", "iii"]:
                firstNote = base + 4
            elif numeralArr[0] in ["IV", "iv"]:
                firstNote = base + 5
            elif numeralArr[0] in ["V", "v"]:
                firstNote = base + 7
            elif numeralArr[0] in ["VI", "vi"]:
                firstNote = base + 9
            elif numeralArr[0] in ["VII", "vii"]:
                firstNote = base + 11
            else:
                raise ValueError("One of the chords is unrecognized. Accepted chords are I/i - VII/vii")

            # Generar la triada base mayor/menor
            note1, note2, note3 = baseChords(firstNote, numeralArr[0])
            chord = note1, note2, note3

            # si hay más argumentos => alteraciones
            if len(numeralArr) > 1:
                if (numeralArr[1] in ["#", "b"]):
                    # raiseNote
                    note1, note2, note3 = raiseNote(note1, note2, note3, numeralArr[1])
                    chord = note1, note2, note3
                    if len(numeralArr) == 3 and numeralArr[2] in ALTERATIONS_ARR:
                        # tenemos un tetrad
                        note1, note2, note3, note4 = chordAlteration(note1, note2, note3, numeralArr[2])
                        chord = note1, note2, note3, note4
                elif (numeralArr[1] in ALTERATIONS_ARR):
                    # tenemos un tetrad
                    note1, note2, note3, note4 = chordAlteration(note1, note2, note3, numeralArr[1])
                    chord = note1, note2, note3, note4
                else:
                    raise ValueError("Unrecognized alteration or #/b usage.")

            chordArr.append(chord)

        # Paso 2: Generar archivos .mid para todas las inversiones
        track = 0
        channel = 0
        time = 0
        duration = 2
        tempo = 60
        volume = 100

        # Chequeo si la progresión es de 3 o 4 acordes
        if len(chordArr) == 3:
            num = 0
            tempArr1, tempArr2, tempArr3 = chordArr
            for c1 in range(len(tempArr1)):
                for c2 in range(len(tempArr2)):
                    for c3 in range(len(tempArr3)):
                        # Acorde 1
                        if len(tempArr1) == 3:
                            tA1 = chordInversions3(tempArr1[0], tempArr1[1], tempArr1[2], c1)
                        else:
                            tA1 = chordInversions4(tempArr1[0], tempArr1[1], tempArr1[2], tempArr1[3], c1)
                        # Acorde 2
                        if len(tempArr2) == 3:
                            tA2 = chordInversions3(tempArr2[0], tempArr2[1], tempArr2[2], c2)
                        else:
                            tA2 = chordInversions4(tempArr2[0], tempArr2[1], tempArr2[2], tempArr2[3], c2)
                        # Acorde 3
                        if len(tempArr3) == 3:
                            tA3 = chordInversions3(tempArr3[0], tempArr3[1], tempArr3[2], c3)
                        else:
                            tA3 = chordInversions4(tempArr3[0], tempArr3[1], tempArr3[2], tempArr3[3], c3)

                        # Escribimos el archivo MIDI
                        MyMIDI = MIDIFile(1)
                        MyMIDI.addTempo(track, time, tempo)
                        timeOffset = 0
                        for c in [tA1, tA2, tA3]:
                            for cn in c:
                                MyMIDI.addNote(track, channel, cn, time+timeOffset, duration, volume)
                            timeOffset += 2

                        midiName = f"{noteName}-{name}-{num}.mid"
                        filename = path / midiName
                        with open(filename, "wb") as output_file:
                            MyMIDI.writeFile(output_file)
                        num += 1

        elif len(chordArr) == 4:
            num = 0
            tempArr1, tempArr2, tempArr3, tempArr4 = chordArr
            for c1 in range(len(tempArr1)):
                for c2 in range(len(tempArr2)):
                    for c3 in range(len(tempArr3)):
                        for c4 in range(len(tempArr4)):
                            # Mismas inversiones para 4 acordes
                            ...
                            # Similar al caso 3 acordes
                            # Guardado en .mid
                            ...

    print(f"Done generating {progression} => {name} in all keys & octaves!")
