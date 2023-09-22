"""
Author:         Coen Konings
Date:           September 12, 2023
Last edited by: Coen Konings
On:             September 19, 2023

main.py:
Given a tempo in BPM and a set of note durations, play the given rhythm.
"""
import simpleaudio as sa
from time import sleep, time
from os.path import isfile
from icecream import ic
from queue import Queue
import threading


def play_sound():
    """
    Play sample.wav once. Wait for the given duration. If the given duration is
    less than 0, wait until playback has finished.
    """
    # From https://simpleaudio.readthedocs.io/en/latest/
    wave_obj = sa.WaveObject.from_wave_file("../assets/sample.wav")
    play_obj = wave_obj.play()


def play_rhythm(timestamps, q):
    """
    Play a rhythm using the given timestamps.
    """
    start_time = time()
    done = False
    i = 0
    print("PLAYING")

    while not done:
        time_since_start = time() - start_time
        done = not q.empty()

        if time_since_start >= timestamps[i]:
            print(time_since_start)
            play_sound()
            i += 1
        else:
            sleep(0.001)

        if i >= len(timestamps):
            start_time = time()
            i = 0


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
        path = input("Path to the sample to be played: (should be a .wav file)\n>")

    return path


def rhythm_input():
    """
    Given the number of times a sample should be played, get the duration for
    each play. Each duration is given using a number, where 1 is a quarter
    note, 0.5 is an eighth note, 0.25 is a sixteenth, etc.
    """
    rhythm = []
    prompt = "Enter the duration for note {}, where 1 is a quarter note. Type Q to stop entering notes.\n>"

    while True:
        duration = input(prompt.format(len(rhythm) + 1))

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


def timestamps_16th_to_timestamps_seconds(timestamps_16th, bpm):
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
    rhythm = rhythm_input()
    timestamps_16th = durations_to_timestamps_16th(rhythm)
    timestamps = timestamps_16th_to_timestamps_seconds(timestamps_16th, bpm)

    q = Queue()
    play_thread = threading.Thread(target=play_rhythm, args=[timestamps, q])
    play_thread.start()

    input("Press enter when you want the rhythm to stop playing.")
    q.put("stop")

    play_thread.join()

    # TODO change tempo during playback
    # TODO multiple samples
    # TODO repeat playback until user indicates they want to quit


if __name__ == "__main__":
    main()
