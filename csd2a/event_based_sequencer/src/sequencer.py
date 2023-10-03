"""
Author:         Coen Konings
Date:           October 3, 2023
Last edited by: Coen Konings
On:             October 3, 2023

sequencer.py:
Implement all classes necessary to run a sequencer.
TODO move functionalities from main.py to appropriate class.
"""


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
        TODO Move to sequencertrack?
        """
        self.audio_file.play()
        print(self)


class SequencerTrack:
    """
    A sequencer track is used to play and track the note events of a rhythm.
    Each sequencer track is dedicated to a single rhythmic instrument with a
    single audio file.
    """

    def __init__(self, length, audio_file):
        """
        Initialize a sequencer track given its length and an audio file.
        """
        self.length = length
        self.note_events = []
        self.audio_file = audio_file
        self.note_index = 0

    def add_note(self, timestamp, audio_file, duration, velocity, replace=False):
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

        self.note_events.append(NoteEvent(timestamp, audio_file, duration, velocity))


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