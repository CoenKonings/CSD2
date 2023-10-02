"""
Author:         Coen Konings
Date:           September 29, 2023
Last edited by: Coen Konings
On:             September 29, 2023

main.py:
Given a tempo in BPM, a set of audio files and a set of note durations, play a
rhythm.

TODO
- Create Sequencer class.
"""
import simpleaudio as sa
from time import sleep, time
from os.path import isfile
from queue import Queue
import threading


class NoteEvent:
    """
    A class that holds information on a note event, including timestamp, audio
    file, duration and velocity.
    """

    def __init__(self, timestamp, audio_file, duration, velocity):
        """
        Initialize a note object.
        """
        self.timestamp = timestamp
        self.audio_file = audio_file
        self.duration = duration # Duration in 16th notes.
        self.velocity = velocity

    def __str__(self):
        """
        Return a string representation of this note event.
        """
        return "<Note event object. Timestamp: {}. Audio file: {}. Duration: {}. Velocity: {}.>".format(self.timestamp, self.audio_file, self.duration, self.velocity)

    def __lt__(self, other):
        """
        Return true if this note event's timestamp is smaller than the other's.
        Return false otherwise.
        """
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        """
        Return true if both note events occur simultaneously.
        """
        return self.timestamp == other.timestamp

    def sixteenth_duration(self, bpm):
        """
        Return the duration of a sixteenth note.
        """
        return 15 / bpm

    def timestamp_in_seconds(self, bpm):
        """
        Given a list containing timestamps in sixteenth notes and the bpm, return
        a list containing timestamps in seconds.
        """
        return self.sixteenth_duration(bpm) * self.timestamp

    def duration_in_seconds(self, bpm):
        return self.sixteenth_duration(bpm) * self.duration

    def is_ready_to_play(self, time_since_start, bpm):
        """
        Return True if this NoteEvent is ready to be played. Return False
        otherwise.
        """
        return self.timestamp_in_seconds(bpm) <= time_since_start

    def play(self):
        """
        Play this event's sound if current time exceeds this note event's
        timestamp.
        """
        self.audio_file.play()


def play_rhythm(note_events, bpm, q):
    """
    Play a rhythm using the given timestamps.
    """
    start_time = time()
    done = False
    i = 0

    while not done:
        time_since_start = time() - start_time

        try:
            command = q.get(block=False)
        except:
            command = None

        if command == "stop":
            done = True
        elif isinstance(command, int):
            bpm = command
            start_time = time() - note_events[i].timestamp_in_seconds(bpm) + 0.001
            continue

        if note_events[i].is_ready_to_play(time_since_start, bpm):
            note_events[i].play()
            i += 1
        else:
            sleep(0.001)

        if i == len(note_events):
            start_time = time() + note_events[-1].duration_in_seconds(bpm)
            i = 0


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


def sample_path_input():
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

        if duration.lower() == "q":
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


def input_while_playing(queue):
    """
    Get input from the user and send it into the queue.
    """
    while True:
        command = input("Q to stop playing, or a positive integer to change the BPM.\n>")

        if (command.lower() == "q"):
            queue.put("stop")
            break
        elif str_is_int_gt_zero(command):
            queue.put(int(command))


def note_events_input():
    """
    Given an audio file and a rhythm, create the appropriate note events.
    Repeat until the user indicates they are done.
    """
    done = False
    note_events = []

    while not done:
        sample_path = sample_path_input()
        rhythm = rhythm_input()
        timestamps_16th = durations_to_timestamps_16th(rhythm)

        for i in range(len(rhythm)):
            note_events.append(NoteEvent(timestamps_16th[i], sa.WaveObject.from_wave_file(sample_path), rhythm[i] * 4, 100))

        done = input("Enter a rhythm for another sample? Y for yes, any other key for no.\n>").lower() != "y"

    return note_events


def sort_note_events(note_events):
    """
    Sort a list of note events by ascending timestamps.
    """
    return sorted(note_events, reverse=False)


def main():
    """
    Play a rhythm defined by the user.
    """
    bpm = bpm_input()
    note_events = note_events_input()
    note_events = sort_note_events(note_events)

    q = Queue()
    play_thread = threading.Thread(target=play_rhythm, args=[note_events, bpm, q])

    try:
        play_thread.start()
        input_while_playing(q)
    except KeyboardInterrupt:
        q.put("stop")

    play_thread.join()
    print("Bye!")


if __name__ == "__main__":
    main()
