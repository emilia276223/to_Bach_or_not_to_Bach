import os
from music21 import converter, tempo


def get_first_measure_tempo_in_directory(directory):
    """
    Checks the tempo of the first measure in each MIDI file in a directory using music21.

    Args:
        directory (str): Path to the directory containing MIDI files.

    Prints:
        For each file, the tempo (in beats per minute) of the first measure, or 'ERROR' if not specified.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.mid') or filename.endswith('.midi'):
            file_path = os.path.join(directory, filename)
            try:
                # Load the MIDI file
                midi_data = converter.parse(file_path)

                # Find the tempo indication in the first measure
                first_measure = midi_data.measures(0, 1)
                for elem in first_measure.recurse():
                    if isinstance(elem, tempo.MetronomeMark):
                        # print(f"{filename}: The tempo of the first measure is {elem.number} BPM.")
                        break
                else:
                    # Print ERROR if no tempo is found
                    print(f"{filename}: ERROR")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

