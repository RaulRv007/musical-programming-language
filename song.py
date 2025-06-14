from music21 import *

class Note:
    def __init__(self, degree, isChord=False, figure='whole', notes=None, staccato=False, isRest=False):
        self.degree = degree
        self.isChord = isChord
        self.figure = figure
        self.notes = notes or []
        self.staccato = staccato
        self.isRest = isRest

class Song:
    def __init__(self, file):
        self.file = file
        self.score = converter.parse(file)
        self.processed = self.analyze()

    def analyze(self):
        key = self.score.analyze('key')
        print(f"Estimated Key: {key.tonic.name} {key.mode}\n")

        analysis_lines = []
        processed = []

        for element in self.score.recurse().notesAndRests:
            time = element.offset
            base_type = element.duration.type
            dots = element.duration.dots
            figure = base_type + ("." * dots)

            # Check for irregular tuplets (triplets etc.)
            if element.duration.tuplets:
                for tuplet in element.duration.tuplets:
                    if tuplet.tupletActual != tuplet.tupletNormal:
                        figure += "t"
                        break

            staccato = False
            notes = []
            roman_name = ""

            if isinstance(element, note.Note):
                notes = [str(element.pitch)]
                staccato = any(isinstance(art, articulations.Staccato) for art in element.articulations)
                roman_name = self.get_roman_from_pitch(element, key)

            elif isinstance(element, chord.Chord):
                notes = [str(p) for p in element.pitches]
                staccato = any(isinstance(art, articulations.Staccato) for n in element.notes for art in n.articulations)
                roman_name = self.get_roman_from_chord(element, key)

            elif isinstance(element, note.Rest):
                notes = ["Rest"]
                roman_name = "–"

            else:
                continue  # unknown element

            # Add staccato marker to figure
            if staccato:
                figure += "s"

            is_chord = isinstance(element, chord.Chord)
            is_chord = is_chord and len(notes) > 1
            is_rest = isinstance(element, note.Rest)
            is_rest = is_rest and len(notes) == 1 and notes[0] == "Rest"

            processed.append(Note(degree=roman_name, isChord=is_chord, figure=figure, notes=notes, staccato=staccato, isRest=is_rest))
            line = f"{time:>5} | {figure:<11} | {roman_name:<14} | {notes}"
            analysis_lines.append(line)


        return processed

    def get_roman_from_chord(self, chord_obj, key):
        try:
            rn = roman.romanNumeralFromChord(chord_obj, key)
            return rn.figure
        except:
            return "?"

    def get_roman_from_pitch(self, note_obj, key):
        try:
            scale_degrees = key.getScale().getScaleDegreeFromPitch(note_obj.pitch)
            return str(scale_degrees) if scale_degrees else "?"
        except:
            return "?"
