from music21 import converter, stream, chord, tempo, key, instrument, note
import numpy as np
# import pretty_midi
import json




# The program gets all the features we want to use as data 
# to train and test the models from the MIDI file. 
# The progam writes the data to the output file as json


# Tempo
# We want to calculate 3 values:
# * Average tempo of the entire piece
# * Rubato:
#     * Maximum tempo changes within a measure
#     * Average number of tempo changes per measure
#     * Number of measures with tempo changes
def tempo_elements (midi_stream):
    return midi_stream.flatten().getElementsByClass(tempo.MetronomeMark)


# the average tempo:
def average_tempo (midi_stream):
    tempo_elems = tempo_elements(midi_stream)
    tempos = [el.number for el in tempo_elems if el.number is not None]
    return sum(tempos) / len(tempos) if tempos else None
    
# the rubato:
def rubato (midi_stream):
    measure_tempo_changes = []
    for measure in midi_stream.parts[0].getElementsByClass(stream.Measure):
        # Find tempo changes within the measure
        measure_tempos = measure.flatten().getElementsByClass(tempo.MetronomeMark)
        measure_tempo_changes.append(len(measure_tempos))
        
    max_tempo_changes = max(measure_tempo_changes) if measure_tempo_changes else 0
    average_tempo_changes = sum(measure_tempo_changes) / len(measure_tempo_changes) if measure_tempo_changes else 0
    measures_with_changes = sum(1 for changes in measure_tempo_changes if changes > 0)
    return { "max_tempo_changes": max_tempo_changes,
            "average_tempo_changes": average_tempo_changes,
            "measures_with_changes": measures_with_changes}


# Pitches 
def get_pitches (midi_stream):
    return [note.pitches for note in midi_stream.flatten().notes]
# print(midi_stream.flatten().notes[0])

# the average number of pithes at the same time:
# this value will show us if there are many notes played
# that start at the same time
def pitches_and_number_of_pitches_average(midi_stream):
    num_of_pitches = []
    pitches = []
    for p in get_pitches(midi_stream):
        temp = []
        for el in p:
            temp.append(str(el))
        pitches.append(temp)
        num_of_pitches.append(len(temp)) 
        # there is no point in converting it back to tuple 
        # since jsonifying will make it a list anyway

    return pitches, (sum(num_of_pitches) / len(num_of_pitches))

        
# normalized pitches: (with pretty_midi)
def pitches_normalized(filename):
    import pretty_midi
    p_midi_data = pretty_midi.PrettyMIDI(filename)

    # We iterate by instruments and notes
    all_pitches = [] # all pitches
    for inst in p_midi_data.instruments:
        for i_note in inst.notes:
            # notes are already written as integer of 0 - 127 so we normalize them by dividing by 128
            all_pitches.append(i_note.pitch)
    return [x/128 for x in all_pitches]


# Instruments (we will not save the program since not all instruments have one)
def instruments(midi_stream, filename):
    instrums = []
    for part in midi_stream.parts:
        part_instruments = part.getElementsByClass(instrument.Instrument)
        if len(part_instruments) > 0:
            for inst in part_instruments:
                instrums.append((inst.instrumentName))
        else:
            first_measure = part.measures(0, 1)
            # Check for the instruments in the first measure
            for element in first_measure.flatten():
                if isinstance(element, instrument.Instrument):
                    instrums.append((element.instrumentName))
            # part_instruments = first_measure.getElementsByClass(instrument.Instrument)
            # if part_instruments:  # Jeśli znaleziono instrumenty
            #     for inst in part_instruments:
            #         instruments.append((inst.instrumentName, inst.program))
    if len(instrums) == 0:
        print("Nie znaleziono instrumentów w pliku ", filename)
    else: 
        print("all good")


# Key signature
def key_signature(midi_stream):
    key_sig = midi_stream.analyze('key')
    # sharps - gives us a number of # or b which combined with the fact
    # if the key is dur or moll (major/minor) defines the original key 
    # signature and we can easly represent it by numbers
    return (key_sig.sharps, key_sig.mode == "major") 



# duration of the notes
def duration_of_notes(midi_stream):
    note_durations = []
    for element in midi_stream.flatten().notes:
        if isinstance(element, note.Note):
            note_durations.append(str(element.quarterLength))
    return note_durations


# dynamics of the piece (velocities)
def dynamics(midi_stream):
    velocities = []
    for element in midi_stream.flatten().notes:
        if isinstance(element, note.Note):
            velocities.append(element.volume.velocity)
    return velocities



# get all the information to a dictionary
def prepare_dict(midi_stream, filename):
    data = {}
    data["average_tempo"] = average_tempo(midi_stream)
    data["rubato"] = rubato(midi_stream)   
    data["pitches"], data["average_of_pitches"] = pitches_and_number_of_pitches_average(midi_stream)
    data["pitches_normalized"] = pitches_normalized(filename)
    data["instruments"] = instruments(midi_stream, filename)
    data["key_signature"] = key_signature(midi_stream)
    data["note_durations"] = duration_of_notes(midi_stream)
    data["velocities"] = dynamics(midi_stream)
    return data



# run the program
# filename = input()
filename = 'features/chp_op18.mid'
output_file = (filename[0:-4])+'.json'

midi_stream = converter.parse(filename)

data = prepare_dict(midi_stream, filename)

# write the JSON to a specific file
with open(output_file, 'w') as fd:
    json.dump(data, fd)
