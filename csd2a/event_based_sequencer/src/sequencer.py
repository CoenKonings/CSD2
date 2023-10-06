"""
Author:         Coen Konings
Date:           October 3, 2023
Last edited by: Coen Konings
On:             October 3, 2023

sequencer.py:
Implement all classes necessary to run a sequencer.
"""
import simpleaudio as sa
import threading
import time
from helpers import (
    str_is_int_gt_zero,
    note_duration_valid,
    durations_to_timestamps_16th,
)
from os.path import isfile
from queue import Queue


class NoteEvent:
    """
    Note events hold all relevant information on rhythmic notes, such as
    velocity, timestamp and duration.
    """

    def __init__(self, timestamp, audio_file, duration, velocity):
        """
        Initialize a note object given the timestamp in 16th notes, the audio
        file to be played, the duration in 16th notes, and the velocity (a
        number from 0 to 127).
        TODO Move audio file to sequencertrack?
        """
        self.timestamp = timestamp
        self.audio_file = audio_file
        self.duration = duration  # Duration in 16th notes.
        self.velocity = velocity

    def __str__(self):
        """
        Return a string representation of this note event.
        """
        return "<Note event object. Timestamp: {}. Audio file: {}. Duration: {}. Velocity: {}.>".format(
            self.timestamp, self.audio_file, self.duration, self.velocity
        )

    def __lt__(self, other):
        """
        Return true if this note event's timestamp is smaller than the other's.
        Return false otherwise. This function enables sorting by timestamp.
        """
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        """
        Return true if both note events occur simultaneously. This function
        enables sorting by timestamp.
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
        """
        Given a bpm, calculate the duration of a sixteenth note.
        TODO Move to sequencer class probably.
        """
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
        TODO Move audio file to sequencertrack?
        """
        self.audio_file.play()
        print(self)


class SequencerTrack:
    """
    A sequencer track is used to play and track the note events of a rhythm.
    Each sequencer track is dedicated to a single rhythmic instrument with a
    single audio file. Sequencer tracks are mono.
    """

    def __init__(self, length, audio_file):
        """
        Initialize a sequencer track given its length and an audio file.
        """
        self.length = length
        self.note_events = []
        self.audio_file = audio_file
        self.note_index = 0
        self.sixteenth_index = 0

    def add_note(self, timestamp, duration, velocity, replace=False):
        """
        Add a note event. If a note event exists at the given timestamp and
        replace is False, do not insert the new note event. If replace is True,
        replace the old note event with the new note event.
        """
        if any(note_event.timestamp == timestamp for note_event in self.note_events):
            if replace:
                self.note_events = list(
                    filter(
                        lambda note_event: note_event.timestamp != timestamp,
                        self.note_events,
                    )
                )
            else:
                return

        note_event = NoteEvent(timestamp, self.audio_file, duration, velocity)
        self.note_events.append(note_event)
        self.note_events.sort()

    def step(self):
        """
        Step the sequencer track one sixteenth.
        """
        self.sixteenth_index = (self.sixteenth_index + 1) % self.length

        if self.note_events[self.note_index].timestamp == self.sixteenth_index:
            self.note_events[self.note_index].play()
            self.note_index = (self.note_index + 1) % len(self.note_events)


class Sequencer:
    """
    The sequencer is the brain and face of the system. It will keep track of
    time, control the tracks / rhythms and handle user input.
    """

    def __init__(self):
        """
        Initialize the sequencer by creating an empty list of sequencer
        tracks.
        """
        self.tracks = []
        self.bpm = 120
        self.sixteenth_duration = 15 / self.bpm
        self.queue = Queue()

    def bpm_input(self):
        """
        Display the default bpm to the user. If the user wishes to change it, get
        the new bpm.
        """
        user_input = "-1"

        while not str_is_int_gt_zero(user_input) and user_input != "":
            user_input = input(
                "Enter the tempo in bpm. Leave empty for {}bpm.\n>".format(self.bpm)
            )

        if user_input != "":
            self.bpm = int(user_input)
            self.sixteenth_duration = 15 / self.bpm

    def rhythm_input(self):
        """
        Given the number of times a sample should be played, get the duration for
        each play. Each duration is given using a number, where 1 is a quarter
        note, 0.5 is an eighth note, 0.25 is a sixteenth, etc.
        TODO: duration in sixteenths
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

    def audio_file_input(self):
        """
        Get the path to a .wav audio file from the user and set the given file
        as this track's audio file.
        """
        path = ""

        while not (isfile(path) and path.endswith(".wav")):
            path = input("Path to the sample to be played: (should be a .wav file)\n>")

        return sa.WaveObject.from_wave_file(path)

    def notes_input(self):
        """
        Given an audio file and a rhythm, create the appropriate note events.
        Repeat until the user indicates they are done.
        """
        done = False

        while not done:
            audio_file = self.audio_file_input()
            rhythm = self.rhythm_input()
            timestamps_16th = durations_to_timestamps_16th(rhythm)
            track = SequencerTrack(16, audio_file)
            self.tracks.append(track)

            for i in range(len(rhythm)):
                track.add_note(timestamps_16th[i], rhythm[i], 100)

            done = (
                input(
                    "Enter another sequencer track? Y for yes, any other key for no.\n>"
                ).lower()
                != "y"
            )

    def input_while_playing(self):
        """
        Get input from the user and send it into the queue.
        """
        while True:
            command = input(
                "Q to stop playing, or a positive integer to change the BPM.\n>"
            )

            if command.lower() == "q":
                self.queue.put("stop")
                break
            elif str_is_int_gt_zero(command):
                self.queue.put(int(command))

    def play(self):
        """
        Play a rhythm using the given timestamps.
        """
        start_time = time.time()
        done = False
        n_sixteenths = 0

        while not done:
            time_since_start = time.time() - start_time

            try:
                command = self.queue.get(block=False)
            except:
                command = None

            if command == "stop":
                done = True
            elif isinstance(command, int):
                self.bpm = command
                start_time = time.time() + 0.001
                n_sixteenths = 1
                continue

            if time_since_start - n_sixteenths * self.sixteenth_duration > 0:
                [track.step() for track in self.tracks]
                n_sixteenths += 1
            else:
                time.sleep(0.001)

    def start(self):
        """
        Start playing the sequences.
        """
        play_thread = threading.Thread(target=self.play)

        try:
            play_thread.start()
            self.input_while_playing()
        except KeyboardInterrupt:
            self.queue.put("stop")

        play_thread.join()
        print("Bye!")
