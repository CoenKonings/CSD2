"""
Author:         Coen Konings
Date:           September 12, 2023
Last edited by: Coen Konings
On:             September 19, 2023

main.py:
Ask user how many notes they want to enter, after which the user will be able
to enter note durations where 1 is a quarter note, 0.5 is an eighth, etc.
After the notes are entered, the user can enter the BPM at which the rhythm
should be played. Finally, the sample (wav) with which the sample should be
played can be entered. The program then plays the rhythm using the given
sample.
"""
import simpleaudio as sa
from time import sleep
from os.path import isfile


def play_sound(duration=-1, sample_path="../samples/plokrkr.wav"):
    """
    Play sample.wav once. Wait until playback has finished.
    """
    # From https://simpleaudio.readthedocs.io/en/latest/
    wave_obj = sa.WaveObject.from_wave_file(sample_path)
    play_obj = wave_obj.play()

    if duration >= 0:
        sleep(duration)
        play_obj.stop()
    else:
        play_obj.wait_done()


def play_rhythm(rhythm, sample_path):
    """
    Play the sample in the given rhythm at the given bpm.
    """

    for note in rhythm:
        play_sound(note, sample_path)


def quarter_note_duration_from_bpm(bpm):
    """
    Given the bpm, calculate the duration of a quarter note in seconds.
    """
    return 60 / bpm


def note_duration_valid(duration):
    """
    Check if the given string represents a valid float greater than 0.
    """

    try:
        duration = float(duration)
    except:
        return False

    if duration <= 0:
        return False

    return True


def get_sample_path():
    """
    Get the path to a .wav audio file from the user.
    """
    path = ""

    while not (isfile(path) and path.endswith(".wav")):
        path = input("Path to the sample to be played: (should be a .wav file)\n> ")

    return path


def get_rhythm(n_plays):
    """
    Given the number of times a sample should be played, get the duration for
    each play. Each duration is given using a number, where 1 is a quarter
    note, 0.5 is an eighth note, 0.25 is a sixteenth, etc.
    """
    rhythm = []

    while len(rhythm) < n_plays:
        duration = input(
            "Duration for note {}, where 1 is a quarter note:\n> ".format(
                len(rhythm) + 1
            )
        )

        if not note_duration_valid(duration):
            print("Please enter a valid positive number. Example: 1.5")
            continue

        rhythm.append(float(duration))

    return rhythm


def get_int_greater_than_zero(prompt):
    """
    Get an integer greater than 0 from the user.
    """
    user_input = "-1"

    while not (user_input.isnumeric() and int(user_input) > 0):
        user_input = input(prompt)

    return int(user_input)


def main():
    """
    Play a rhythm defined by the user.
    """
    n_plays = get_int_greater_than_zero("How many notes do you want to enter?\n> ")
    rhythm = get_rhythm(n_plays)
    bpm = get_int_greater_than_zero("At what bpm should the rhythm be played?\n> ")
    path_to_sample = get_sample_path()
    quarter_dur = quarter_note_duration_from_bpm(bpm)
    # Calculate durations in seconds for rhythm.
    rhythm = [note * quarter_dur for note in rhythm]
    play_rhythm(rhythm, bpm, path_to_sample)


if __name__ == "__main__":
    main()
