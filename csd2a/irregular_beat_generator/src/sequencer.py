"""
Author:         Coen Konings
Date:           October 3, 2023
Last edited by: Coen Konings
On:             October 17, 2023

sequencer.py:
Implement all classes necessary to run a sequencer.
TODO move all user input features to the live coding environment in main.py.
"""
import simpleaudio as sa
import time
from helpers import (
    str_is_int_gt_zero,
    note_duration_valid,
    durations_to_timestamps_16th,
)
from os.path import isfile


class NoteEvent:
    """
    Note events hold all relevant information on rhythmic notes, such as
    velocity, timestamp and duration.
    """

    def __init__(self, track, timestamp, duration, velocity):
        """
        Initialize a note object given the timestamp in 16th notes, the audio
        file to be played, the duration in 16th notes, and the velocity (a
        number from 0 to 127).
        """
        self.track = track
        self.timestamp = timestamp
        self.duration = duration  # Duration in 16th notes.
        self.velocity = (
            velocity  # NOTE: unused, but might be useful in future iterations.
        )

    def __str__(self):
        """
        Return a string representation of this note event.
        """
        return "<Note event object. Timestamp: {}. Audio file: {}. Duration: {}. Velocity: {}.>".format(
            self.timestamp, self.track.name, self.duration, self.velocity
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

    def play(self):
        """
        Play this event's sound if current time exceeds this note event's
        timestamp.
        """
        self.track.audio_file.play()


class SequencerTrack:
    """
    A sequencer track is used to play and track the note events of a rhythm.
    Each sequencer track is dedicated to a single rhythmic instrument with a
    single audio file. Sequencer tracks are mono.
    """

    def __init__(self, sequencer, length, audio_file, name):
        """
        Initialize a sequencer track given its length and an audio file.
        """
        self.sequencer = sequencer
        self.length = length  # Length in sixteenth notes.
        self.note_events = []
        self.audio_file = audio_file
        self.note_index = 0
        self.sixteenth_index = 0
        self.name = name

    def __str__(self):
        """
        Represent the track as a string.
        """
        return self.name + " track"

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

        note_event = NoteEvent(self, timestamp, duration, velocity)
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

        if self.note_events[self.note_index].timestamp >= self.length:
            self.note_index = 0


class Sequencer:
    """
    The sequencer is the brain of the system. It will keep track of time,
    control the tracks / rhythms and handle user input.
    """

    def __init__(self, queue):
        """
        Initialize the sequencer by creating an empty list of sequencer
        tracks, setting default values for attributes and saving the queue that
        will be used for communication between the live coding environment and
        the sequencer.
        """
        self.tracks = []
        self.initialize_tracks()
        self.set_bpm(120)
        self.meter = (4, 4)
        self.queue = queue
        self.start_time = None
        self.done_playing = False
        self.play_index = 0

    def initialize_tracks(self):
        """
        Initialize tracks for high, mid and low.
        """

        for track_name in ["high", "mid", "low"]:
            audio_file_path = "../assets/{}.wav".format(track_name)
            if not isfile(audio_file_path):
                raise Exception('Audio file "{}" not found.'.format(audio_file_path))

            audio_file = sa.WaveObject.from_wave_file(audio_file_path)
            self.tracks.append(SequencerTrack(self, 16, audio_file, track_name))

    def set_bpm(self, bpm):
        """
        Set the bpm and the new sixteenth note duration.
        """
        self.bpm = bpm
        self.sixteenth_duration = 15 / bpm

    def __str__(self):
        """
        Return this sequencer's status as a string.
        """
        return "Tracks: {}. Meter: {}/{}. Tempo: {}bpm.".format(
            len(self.tracks), self.meter[0], self.meter[1], self.bpm
        )

    def add_track(self, length, audio_file, name):
        """
        Add a new track to this sequencer.
        """
        track = SequencerTrack(self, length, audio_file, name)
        self.tracks.append(track)
        return track

    def handle_command(self, command):
        """
        Handle commands from the queue.
        """
        if not command:
            return

        command = command.split()

        if len(command) == 1 and command[0] == "quit":
            self.done_playing = True
        elif len(command) == 2 and command[0] == "bpm":
            self.set_bpm(command[1])
            self.start_time = time.time() + 0.001
            self.play_index = 1

    def get_command(self):
        """
        Get a command from the queue.
        """
        try:
            return self.queue.get(block=False)
        except:
            return None

    def start(self):
        """
        Starts the sequencer's main loop. This loop handles both incoming
        commands and correctly timing each track's events.
        """
        self.start_time = time.time()
        self.done_playing = False
        self.play_index = 0

        while not self.done_playing:
            time_since_start = time.time() - self.start_time
            command = self.get_command()
            self.handle_command(command)

            if time_since_start - self.play_index * self.sixteenth_duration > 0:
                for track in self.tracks:
                    track.step()

                self.play_index += 1
            else:
                time.sleep(0.001)
