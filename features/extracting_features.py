from music21 import converter, stream, chord, tempo, key, instrument, note
import numpy as np
# import pretty_midi
import json




# The program gets all the features we want to use as data 
# to train and test the models from the MIDI file. 
# The progam writes the data to the output file as JSON


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



# normalized pitches: (with mido)
# We do not want all the pitches (it is a lot of data and
# we cannot use that since every piece has different amount
# of pitvhes). We want some more standarized info:
# * how many notes of each piece are (the pitches are 0 - 127)
# * average pitch
# * ... TODO
def pitches_normalized(filename):
    import mido
    
    midi_data = mido.MidiFile(filename)

    # how many notes of each pitch
    pitch_histogram = [0 for _ in range(128)]
    avg_pitch = 0

    for track in midi_data.tracks:
        for msg in track:
            # for each note (louder than 0)
            if msg.type == 'note_on' and msg.velocity > 0:
                # msg.note is a 1-127 representing pitch
                pitch_histogram[msg.note] += 1
                avg_pitch += msg.note

    avg_pitch /= sum(pitch_histogram)
    return {
        "pitch_histogram" : pitch_histogram,
        "average_pitch": avg_pitch
    }

# Instruments
# Since many different instruments can be in the music piece
# we will count how many of common orchestral instruments are
# and the number of instruments total
def instruments(midi_stream, filename):

    common_instruments = ["Piano", "Flute", "Bassoon", "Double bass", "Clarinet", "Trumpet", "French horn", "Violin", "Cello", "Harp", "Oboe", "Tuba", "Viola", "Piccolo", "Trombone", "Saxophone", "English Horn", "Harpsichord"]
    
    # we will use a dictionary with all the instruments
    found_instruments = {}
    for inst in common_instruments:
        found_instruments[inst] = 0

    number_of_instruments = 0

    # getting instruments from each part
    for part in midi_stream.parts:
        try:
            part_instruments = part.getElementsByClass(instrument.Instrument)
        except Exception as e:
            print("Exception: ", e)
            part_instruments = []
        if len(part_instruments) > 0:
            all_instruments = part_instruments
        else:
            first_measure = part.measures(0, 1)
            all_instruments = filter((lambda x : isinstance(x, instrument.Instrument) ), first_measure.flatten())

        # for each instrument we see where does it fir
        # since sometimes we have more than 1 instrumets of each kind
        # they are mostly named Instrument 1, ... so we will check if the 
        # name of the instrument is contained in what we find:
        for inst in all_instruments:
            number_of_instruments += 1
            for com_inst in common_instruments:
                if com_inst in str(inst):
                    found_instruments[com_inst] += 1

        # just found instruments will not be enought since it
        # might happen that the MIDI has an instrument out of
        # out dataset (it should not happen often)   
        # 
        # for a machine learning model the names will not be needed
        # so instead of a dictionary we can just use a list:     
        return {
            "number_of_instruments": number_of_instruments,
            "types_of_instruments": [found_instruments[x] for x in common_instruments]
        }


# Key signature
def key_signature(midi_stream, filename):
    # since all parts should have the same key we will look for it
    # in the first part in the first measure
    # midi_stream.show('text')
    key_sig = None
    part = midi_stream.parts[0]
    first_measure = part.measures(0, 1)
    # first_measure.show('text')
    for element in first_measure.flatten():
        if isinstance(element, key.Key):
            key_sig = element
            return key_sig.sharps, key_sig.mode == "major"

    # if the key is not written in the part or first measure we 
    # should try in other parts:
    
    if key_sig == None:
        for part in midi_stream.parts[0:]:
            first_measure = part.measures(0, 1)
            for element in first_measure.flatten():
                if isinstance(element, key.Key):
                    key_sig = element
                    return (key_sig.sharps, key_sig.mode == "major") 

    # if the key is still not found: the program  
    # "estimates" it using analyze() function from music21 module
    if key_sig == None:
        key_sig = midi_stream.analyze('key')
        # print('-------------------------------------')
        # print(f"Key estimathed, not found (file = {filename})")
        # print('-------------------------------------')

    # sharps - gives us a number of # or b which combined with the fact
    # if the key is dur or moll (major/minor) defines the original key 
    # signature and we can easly represent it by numbers
    return (key_sig.sharps, key_sig.mode == "major") 



# duration of the notes
# we do not want all the notes so we will get some more
# standarized data such as:
# * average note duration
# * count of all possible durations (the shortest possible is )
def duration_of_notes(midi_stream):
    note_durations = []
    for element in midi_stream.flatten().notes:
        if isinstance(element, note.Note):
            note_durations.append(float(element.quarterLength))

    avg_note_dur = sum(note_durations)/len(note_durations)

    # for a note durations histogram it is better to use .ordinal
    note_dur_options = {"0": 0, "1": 1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, 'complex':11, "inexpressible":12}
    note_dur_hist = [0 for _ in range(len(note_dur_options))]
    
    for element in midi_stream.flatten().notes:
        if isinstance(element, note.Note):
            ord = note_dur_options[str(element.duration.ordinal)]
            note_dur_hist[ord] += 1
    return {
        "average_note_duration": avg_note_dur,
        "note_duration_histogram": note_dur_hist
    }


# dynamics of the piece (velocities)
# the values of velocity are in [0, 127] so
# we will get:
# * histogram of the values
# * average value
def dynamics(midi_stream):
    velocities = [0 for _ in range(128)]
    avg = 0
    for element in midi_stream.flatten().notes:
        if isinstance(element, note.Note):
            velocities[element.volume.velocity] += 1
            avg += element.volume.velocity
    avg = avg / sum(velocities)
    return {
        "velocity_histogram": velocities,
        "average_velocity": avg
    }



# get all the information to a dictionary
def prepare_data(filename):
    # to parse midi file music21 parser is being used
    midi_stream = converter.parse(filename)

    data = {}
    print("Processing ", filename)
    # midi_stream.show('text')
    data["average_tempo"] = average_tempo(midi_stream)
    data["rubato"] = rubato(midi_stream)
    data["pitches_normalized"] = pitches_normalized(filename)
    data["instruments"] = instruments(midi_stream, filename)
    data["key_signature"] = key_signature(midi_stream, filename) 
    data["note_durations"] = duration_of_notes(midi_stream)
    data["velocities"] = dynamics(midi_stream)
    return data



# run the program

# the program takes as an argument a midi file
import sys
if len(sys.argv) == 1: # the first argument is always name of the python file
    filename = 'features/chp_op18.mid'
else:
    filename = sys.argv[1]

# the output file has the same name but .json instead of .mid
output_file = (filename[0:-4])+'.json'


# getting the interesting features from midi
data = prepare_data(filename)

# write the JSON to a specific file
with open(output_file, 'w') as fd:
    json.dump(data, fd)
