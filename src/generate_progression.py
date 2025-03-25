#!/usr/bin/env python

from midiutil import MIDIFile
from pathlib import Path
import random
import json
from .config import MIDI_DIR

NOTE_ARRAY = ["C", "C#", "D", "Eb", "E", "F",
              "F#", "G", "Ab", "A", "Bb", "B"]
OCTAVE_ARRAY = [2, 3, 4, 5]

ALTERATIONS_ARR = [
    "min", "maj", "dim", "aug",
    "min6", "maj6",
    "min7", "minmaj7", "maj7", "7", "dim7", "hdim7",
    "sus2", "sus4"
]

def baseChords(firstNote, numeral):
    if numeral.isupper():
        note1 = firstNote
        note2 = note1 + 4
        note3 = note2 + 3
    else:
        note1 = firstNote
        note2 = note1 + 3
        note3 = note2 + 4
    return note1, note2, note3

def raiseNote(note1, note2, note3, raiseVal):
    if raiseVal == "#":
        return note1 + 1, note2 + 1, note3 + 1
    elif raiseVal == "b":
        return note1 - 1, note2 - 1, note3 - 1

def chordAlteration(note1, note2, note3, ext):
    if ext == "7":
        note4 = note3 + 3
    elif ext == "maj7":
        note4 = note3 + 4
    elif ext == "min7":
        note4 = note3 + 3
    elif ext == "minmaj7":
        note4 = note3 + 4
    elif ext == "dim7":
        note2 -= 1
        note3 -= 1
        note4 = note3 + 3
    elif ext == "hdim7":
        note2 -= 1
        note3 -= 1
        note4 = note3 + 4
    elif ext == "min6":
        note4 = note3 + 5
    elif ext == "maj6":
        note4 = note3 + 4
    elif ext == "sus2":
        note2 = note1 + 2
        note3 = note1 + 7
        return note1, note2, note3
    elif ext == "sus4":
        note2 = note1 + 5
        note3 = note1 + 7
        return note1, note2, note3
    elif ext == "dim":
        note2 = note1 + 3
        note3 = note2 + 3
        return note1, note2, note3
    elif ext == "aug":
        note2 = note1 + 4
        note3 = note2 + 4
        return note1, note2, note3
    elif ext == "maj":
        note2 = note1 + 4
        note3 = note2 + 3
        return note1, note2, note3
    elif ext == "min":
        note2 = note1 + 3
        note3 = note2 + 4
        return note1, note2, note3
    else:
        raise ValueError(f"[chordAlteration] Sufijo no reconocido: {ext}")
    return note1, note2, note3, note4

def chordInversions3(note1, note2, note3, inv):
    if inv == 1:
        note1 += 12
    elif inv == 2:
        note1 += 12
        note2 += 12
    elif inv == 3:
        # octava: subir las tres notas
        note1 += 12
        note2 += 12
        note3 += 12
    return note1, note2, note3

def chordInversions4(note1, note2, note3, note4, inv):
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
    progChords = progression.split("-")
    if len(progChords) not in [3, 4]:
        raise ValueError("Only 3- or 4-chord progressions are supported.")

    output_path = Path(output_dir) / name
    output_path.mkdir(parents=True, exist_ok=True)

    nameArray = [f"{n}-{o}" for o in OCTAVE_ARRAY for n in NOTE_ARRAY]
    durations_dict = {}

    for idx, noteName in enumerate(nameArray):
        base_midi = 24 + idx
        chordArr = []

        for numeral in progChords:
            numeralArr = numeral.split(',')
            numeral_base = numeralArr[0]
            firstNote = base_midi + ["I", "II", "III", "IV", "V", "VI", "VII"].index(numeral_base.upper()) * 2
            note1, note2, note3 = baseChords(firstNote, numeral_base)
            chord = (note1, note2, note3)

            if len(numeralArr) > 1:
                token = numeralArr[1]
                if token in ["#", "b"]:
                    note1, note2, note3 = raiseNote(note1, note2, note3, token)
                    chord = (note1, note2, note3)
                    if len(numeralArr) == 3 and numeralArr[2] in ALTERATIONS_ARR:
                        chord = chordAlteration(note1, note2, note3, numeralArr[2])
                elif token in ALTERATIONS_ARR:
                    chord = chordAlteration(note1, note2, note3, token)
                else:
                    raise ValueError(f"[generate_progression] Token no reconocido: {token} en numeral {numeral}")

            chordArr.append(chord)

        track = 0
        channel = 0
        volume = 100

        def random_duration():
            return round(random.uniform(0.5, 2.0), 2)

        def add_chord(MyMIDI, inv, timeOffset, duration):
            for note in inv:
                MyMIDI.addNote(track, channel, note, timeOffset, duration, volume)
            return duration

        num = 0
        if len(chordArr) == 3:
            num_inversions = 4 if len(chordArr[0]) == 3 else 4  # triadas con octava adicional
            for c1 in range(num_inversions):
                for c2 in range(num_inversions):
                    for c3 in range(num_inversions):
                        MyMIDI = MIDIFile(1)
                        MyMIDI.addTempo(track, 0, tempo)
                        timeOffset = 0
                        durations = []
                        for chord_data, c in zip(chordArr, [c1, c2, c3]):
                            dur = random_duration()
                            durations.append(dur)
                            if len(chord_data) == 3:
                                inv = chordInversions3(*chord_data, c)
                            else:
                                inv = chordInversions4(*chord_data, c)
                            timeOffset += add_chord(MyMIDI, inv, timeOffset, dur)
                        filename = f"{noteName}-{name}-{num}.mid"
                        filepath = output_path / filename
                        with open(filepath, "wb") as outmidi:
                            MyMIDI.writeFile(outmidi)
                        durations_dict[filename] = durations
                        num += 1

        elif len(chordArr) == 4:
            num_inversions = 4
            for c1 in range(num_inversions):
                for c2 in range(num_inversions):
                    for c3 in range(num_inversions):
                        for c4 in range(num_inversions):
                            MyMIDI = MIDIFile(1)
                            MyMIDI.addTempo(track, 0, tempo)
                            timeOffset = 0
                            durations = []
                            for chord_data, c in zip(chordArr, [c1, c2, c3, c4]):
                                dur = random_duration()
                                durations.append(dur)
                                if len(chord_data) == 3:
                                    inv = chordInversions3(*chord_data, c)
                                else:
                                    inv = chordInversions4(*chord_data, c)
                                timeOffset += add_chord(MyMIDI, inv, timeOffset, dur)
                            filename = f"{noteName}-{name}-{num}.mid"
                            filepath = output_path / filename
                            with open(filepath, "wb") as outmidi:
                                MyMIDI.writeFile(outmidi)
                            durations_dict[filename] = durations
                            num += 1

    durations_path = output_path / "durations.json"
    with open(durations_path, "w") as f:
        json.dump(durations_dict, f, indent=2)

    print(f"Generated progression '{progression}' -> folder: {output_path}")
