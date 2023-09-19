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
from icecream import ic


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


def sixteenth_note_duration_from_bpm(bpm):
    """
    Given the bpm, calculate the duration of a quarter note in seconds.
    """
    return 15 / bpm


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


def get_rhythm():
    """
    Given the number of times a sample should be played, get the duration for
    each play. Each duration is given using a number, where 1 is a quarter
    note, 0.5 is an eighth note, 0.25 is a sixteenth, etc.
    """
    rhythm = []

    while True:
        duration = input(
            "Enter the duration for note {}, where 1 is a quarter note, or Q to stop entering notes.\n> ".format(
                len(rhythm) + 1
            )
        )

        if duration == "Q":
            if len(rhythm) == 0:
                print("Please enter at least one note.")
                continue

            break

        if not note_duration_valid(duration):
            print("Please enter a valid positive number. Example: 1.5")
            continue

        rhythm.append(float(duration))

    return rhythm


def str_is_int_gt_zero(str):
    """
    Return true if the given string represents an integer larger than 0. Return
    false otherwise.
    """
    return str.isnumeric() and int(str) > 0


def get_int_greater_than_zero(prompt):
    """
    Get an integer greater than 0 from the user.
    """
    user_input = "-1"

    while not str_is_int_gt_zero(user_input):
        user_input = input(prompt)

    return int(user_input)


def bpm_input():
    """
    Display the default bpm to the user. If the user wishes to change it, get
    the new bpm.
    """
    user_input = "-1"

    while not str_is_int_gt_zero(user_input) and user_input != "":
        user_input = input("Enter the tempo in bpm. Leave empty for 120bpm.\n>")

    return 120 if user_input == "" else int(user_input)


def durations_to_timestamps_16th(durations):
    """
    Given a list of durations where 1 is a quarter note, 0.5 is an eighth, etc.
    calculate a list of timestamps.
    """
    total = 0
    timestamps = []

    for duration in durations:
        timestamps.append(total)
        total += duration * 4

    return timestamps


def timestamp_16th_to_timestamp_seconds(timestamps_16th, bpm):
    """
    Given a list containing timestamps in sixteenth notes and the bpm, return
    a list containing timestamps in seconds.
    """
    sixteenth_duration = sixteenth_note_duration_from_bpm(bpm)
    return [sixteenth_duration * timestamp for timestamp in timestamps_16th]


def main():
    """
    Play a rhythm defined by the user.
    """
    bpm = bpm_input()
    rhythm = get_rhythm()
    timestamps_16th = durations_to_timestamps_16th(rhythm)
    timestamps = timestamp_16th_to_timestamp_seconds(timestamps_16th)
    # TODO play rhythm
    # TODO multiple samples
    # TODO change tempo during playback
    # TODO repeat playback until user indicates they want to quit


if __name__ == "__main__":
    main()
