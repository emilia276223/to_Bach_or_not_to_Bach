# normalized pitches: (with mido)
def pitches_normalized(filename):
    import mido

    midi_data = mido.MidiFile(filename)
    all_pitches = []

    for track in midi_data.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                all_pitches.append(msg.note)

    return [x / 128 for x in all_pitches]