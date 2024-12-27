from music21 import converter, stream, chord, tempo, key, instrument, note
import numpy as np
# import pretty_midi
import json

filename = 'chp_op18.mid'
output_fn = 'chp_op18.json'

midi_stream = converter.parse(filename)

# Plan
# basen on the file (op 18th of Chopin for now) the
# program counts all the features we want to use as data 
# to train and test the models. The progam writes the data
# to the file as json


data = {}

# # Chords - at the moment we will not use that
# print("Chords:")
# for element in midi_stream.flat.getElementsByClass('Chord'):
#     print(f"Chord: {element.pitchedCommonName}, Start: {element.offset}, Duration: {element.quarterLength}")


# Tempo
# print("\nTempo:")
# We want to calculate 3 values:
# * Average tempo of the entire piece
# * Rubato:
#     * Maximum tempo changes within a measure
#     * Average number of tempo changes per measure
#     * Number of measures with tempo changes
tempo_elements = midi_stream.flatten().getElementsByClass(tempo.MetronomeMark)
# for t in tempo_elements:
    # print(f"Tempo: {t.getQuarterBPM()} BPM, Start: {t.offset}")
# the number of measures: 

# the average tempo:
tempos = [el.number for el in tempo_elements if el.number is not None]
average_tempo = sum(tempos) / len(tempos) if tempos else None
data["average_tempo"] = average_tempo

# the rubato:
measure_tempo_changes = []
for measure in midi_stream.parts[0].getElementsByClass(stream.Measure):
    # Find tempo changes within the measure
    measure_tempos = measure.flatten().getElementsByClass(tempo.MetronomeMark)
    measure_tempo_changes.append(len(measure_tempos))
    
max_tempo_changes = max(measure_tempo_changes) if measure_tempo_changes else 0
average_tempo_changes = sum(measure_tempo_changes) / len(measure_tempo_changes) if measure_tempo_changes else 0
measures_with_changes = sum(1 for changes in measure_tempo_changes if changes > 0)

data["rubato"] = {
    "max_tempo_changes": max_tempo_changes,
    "average_tempo_changes": average_tempo_changes,
    "measures_with_changes": measures_with_changes
}

# Pitches 
pitches = [note.pitches for note in midi_stream.flatten().notes]
# print(midi_stream.flatten().notes[0])
data["pitches"] = []

#average number of pithes at the same time: (so how many acords)
num_of_pitches = []

for p in pitches:
    temp = []
    for el in p:
        temp.append(str(el))
    data["pitches"].append(temp)
    num_of_pitches.append(len(temp)) 
    # there is no point in convering it back to tuple 
	# since jsonifying will make it a list anyway

num_of_pitches_average = sum(num_of_pitches) / len(num_of_pitches)
data["average_of_pitches"] = num_of_pitches_average
    
        
# normalized pitches: (with pretty_midi)
import pretty_midi
p_midi_data = pretty_midi.PrettyMIDI('chp_op18.mid')

# Iteracja przez instrumenty i nuty
temp = [] # all pitches
for inst in p_midi_data.instruments:
    for i_note in inst.notes:
        # print(note.pitch)
        # notes are already written as integer of 0 - 127 so we normalize them by dividing by 128
        temp.append(i_note.pitch)
data["pitches_normalized"] = [x/128 for x in temp]

# midi_stream.show('text')

# Instruments (we will not save the program since not all instruments have one)
instruments = []
print("\nInstrumenty w utworze:")
for part in midi_stream.parts:
    part_instruments = part.getElementsByClass(instrument.Instrument)
    if len(part_instruments) > 0:
        for inst in part_instruments:
            instruments.append((inst.instrumentName))
    else:
        first_measure = part.measures(0, 1)
        # Szukaj instrumentów w pierwszym takcie
        for element in first_measure.flatten():
            if isinstance(element, instrument.Instrument):
                instruments.append((element.instrumentName))
        # part_instruments = first_measure.getElementsByClass(instrument.Instrument)
        # if part_instruments:  # Jeśli znaleziono instrumenty
        #     for inst in part_instruments:
        #         instruments.append((inst.instrumentName, inst.program))
        
print(instruments)
if len(instruments) == 0:
	print("Nie znaleziono instrumentów")
data["instruments"] = instruments


# Key signature
print("\nKey signature (Tonacja utworu:)")
key_signature = midi_stream.analyze('key')
# sharps - gives us a number of # or b which combined with the fact
# if the key is dur or moll (major/minor) defines the original key 
# signature and we can easly represent it by numbers
data["key_signature"] = (key_signature.sharps, key_signature.mode == "major") 



# duration of the notes
note_durations = []
for element in midi_stream.flatten().notes:
    if isinstance(element, note.Note):
        note_durations.append(str(element.quarterLength))
data["note_durations"] = note_durations

# dynamika utworu
velocities = []
for element in midi_stream.flatten().notes:
    if isinstance(element, note.Note):
        velocities.append(element.volume.velocity)
data["velocities"] = velocities

# write the JSON to a specific file
with open(output_fn, 'w') as fd:
    json.dump(data, fd)
