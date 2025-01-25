import os
from music21 import converter, note, chord


def check_first_measure_for_rests(base_directory):
    """
    For each MIDI file in the given base directory (including subdirectories),
    check if the first measure in every track contains only rests.

    Args:
        base_directory (str): Path to the base directory containing subdirectories
                              of composers with MIDI files.
    """
    for composer_folder in os.listdir(base_directory):
        composer_path = os.path.join(base_directory, composer_folder)
        if os.path.isdir(composer_path):  # Check if it's a folder
            for filename in os.listdir(composer_path):
                if filename.endswith('.mid') or filename.endswith('.midi'):
                    file_path = os.path.join(composer_path, filename)
                    try:
                        # Load the MIDI file using music21
                        midi_data = converter.parse(file_path)
                        all_rests = True  # Assume all rests initially

                        for part in midi_data.parts:
                            # Extract notes and rests from the first measure
                            first_measure = part.measures(0, 1)

                            # Analyze each element in the first measure
                            for elem in first_measure.recurse():
                                # If there's a Note or a Chord, it's not all rests
                                if isinstance(elem, note.Note) or isinstance(elem, chord.Chord):
                                    all_rests = False
                                    break  # No need to check further

                            if not all_rests:
                                break  # Exit if any track doesn't meet the criteria

                            # Output the result
                        if all_rests:
                            print(f"{file_path}")
                        # else:
                            # print(i)

                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
