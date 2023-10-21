"""
Author:         Coen Konings
Date:           October 3, 2023
Last edited by: Coen Konings
On:             October 21, 2023

sequencer.py:
Implement all classes necessary to run a sequencer.
"""
import simpleaudio as sa
import time
from os.path import isfile
from markov import MarkovChain
from helpers import rhythm_file_path
from midiutil import MIDIFile


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
        # NOTE velocity could be used here in a future version.
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
        self.next_rhythm = None
        self.next_length = None
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

    def swap_rhythms(self):
        """
        If a next rhythm exists, edit the list of note events to reflect the
        new rhythm.
        """
        self.note_events = []

        for timestamp in self.next_rhythm:
            self.add_note(timestamp, 1, 100)

        self.next_rhythm = None

    def step(self):
        """
        Step the sequencer track one sixteenth.
        """
        self.sixteenth_index = (self.sixteenth_index + 1) % self.length

        if len(self.note_events) > 0 and self.note_events[self.note_index].timestamp == self.sixteenth_index:
            self.note_events[self.note_index].play()
            self.note_index = (self.note_index + 1) % len(self.note_events)


        if len(self.note_events) > 0 and self.note_events[self.note_index].timestamp >= self.length:
            self.note_index = 0

        if self.note_index == 0 and self.next_rhythm:
            self.swap_rhythms()

        if self.note_index == 0 and self.next_length:
            self.length = self.next_length
            self.next_length = None

    def set_next_rhythm(self, timestamps):
        """
        Set the rhythmical pattern to switch to at the end of the loop.
        """
        self.next_rhythm = timestamps


class Sequencer:
    """
    The sequencer is the brain of the system. It will keep track of time,
    control the tracks / rhythms and handle user input.
    """

    def __init__(self, queue_incoming, queue_outgoing):
        """
        Initialize the sequencer by creating an empty list of sequencer
        tracks, setting default values for attributes and saving the queue that
        will be used for communication between the live coding environment and
        the sequencer.
        """
        self.tracks = []
        self.meter = (7, 8)
        self.markov_chain = MarkovChain()
        self.markov_chain.from_rhythm_file(rhythm_file_path(self.meter))
        self.initialize_tracks()
        self.set_bpm(120)
        self.queue_incoming = queue_incoming
        self.queue_outgoing = queue_outgoing
        self.start_time = None
        self.done_playing = False
        self.play_index = 0

    def __str__(self):
        """
        Return this sequencer's status as a string.
        """
        return "Tracks: {}. Meter: {}/{}. Tempo: {}bpm.".format(
            len(self.tracks), self.meter[0], self.meter[1], self.bpm
        )

    def get_sequence_length(self):
        """
        Calculate the length of the sequence in 16th notes.
        """
        return int(self.meter[0] * 16 / self.meter[1])

    def initialize_tracks(self):
        """
        Initialize tracks for high, mid and low.
        """

        for track_name in ["high", "mid", "low"]:
            audio_file_path = "../assets/{}.wav".format(track_name)

            # Check if required audio file exists.
            if not isfile(audio_file_path):
                raise Exception('Audio file "{}" not found.'.format(audio_file_path))

            audio_file = sa.WaveObject.from_wave_file(audio_file_path)
            self.tracks.append(SequencerTrack(self, self.get_sequence_length(), audio_file, track_name))

    def set_bpm(self, bpm):
        """
        Set the bpm and the new sixteenth note duration.
        """
        self.bpm = bpm
        self.sixteenth_duration = 15 / bpm

    def set_meter(self, numerator, denominator):
        """
        Set the sequencer's and all tracks' meter to numerator/denominator (eg.
        a 7/8 meter has a numerator of 7 and a denominator of 8)
        """
        self.meter[0] = numerator
        self.meter[1] = denominator
        self.markov_chain.from_rhythm_file(rhythm_file_path(self.meter))

        for track in self.tracks:
            track.length = self.get_sequence_length() # Track length in 16ths

    def add_track(self, length, audio_file, name):
        """
        Add a new track to this sequencer.
        """
        track = SequencerTrack(self, length, audio_file, name)
        self.tracks.append(track)
        return track

    def get_track(self, track_name):
        """
        Get a track by name.
        """
        return next((track for track in self.tracks if track.name == track_name), None)

    def handle_bpm_command(self, bpm):
        """
        Set the sequencer's bpm and communicate to the live coding environment
        that it can continue.
        """
        self.set_bpm(bpm)
        self.start_time = time.time() + 0.001
        self.play_index = 1
        self.queue_outgoing.put("done")

    def generate_rhythm(self, track_name, length):
        """
        Generate a rhythm of the given length for the given track.
        """
        new_rhythm = []

        for i in range(length):
            self.markov_chain.step()

            if i == 6 and self.meter == (5, 4) or i == 8 and self.meter == (7, 8):
                self.markov_chain.set_state("mid")

            if self.markov_chain.state.name == track_name:
                new_rhythm.append(i)

        return new_rhythm

    def regenerate_rhythm(self, track_name):
        """
        Generate a new rhythm for the given track.
        TODO cleanup crew
        """

        # Regenerate all tracks. TODO: find a better way?
        if track_name == "all":
            for track in ["low", "mid", "high"]:
                self.regenerate_rhythm(track)
            return

        self.markov_chain.state = None
        track = self.get_track(track_name)
        new_rhythm = self.generate_rhythm(track_name, self.get_sequence_length())
        track.set_next_rhythm(new_rhythm)

    def export_midi(self, file_name):
        """
        Export the current rhythm to a midi track. Source:
        https://pypi.org/project/MIDIUtil/
        """
        midi_file = MIDIFile(1, removeDuplicates=False)
        midi_track = 0
        time = 0
        midi_file.addTrackName(midi_track, time, "Rhythm Track")
        midi_file.addTempo(midi_track, time, self.bpm)
        pitch = 48

        for track_name in ["low", "mid", "high"]:
            track = self.get_track(track_name)

            for note_event in track.note_events:
                midi_file.addNote(midi_track, 0, pitch, note_event.timestamp / 4, 0.25, note_event.velocity)

            pitch += 1 # Separate pitch for each track in the sequencer.

        with open(file_name, "wb") as output_file:
            midi_file.writeFile(output_file)

    def metric_modulation(self):
        """
        Modulate from a 7/8 rhythm to 5/4 or vice versa.
        """
        # Set new meter
        self.meter = (5, 4) if self.meter == (7, 8) else (7, 8)
        # Generate new markov chain using meter
        self.markov_chain.from_rhythm_file(rhythm_file_path(self.meter))
        # Regenerate mid and low tracks
        self.regenerate_rhythm("mid")
        self.regenerate_rhythm("low")

        # Extend high track if necessary
        if self.meter == (5, 4):
            track = self.get_track("high")
            self.markov_chain.set_state("high")
            # Add 6 16th notes to go from 7/8 to 5/4.
            extra_notes = self.generate_rhythm("high", 6)

            for timestamp in extra_notes:
                # Add rhythm to the end of the track
                track.add_note(timestamp + 14, 1, 100)

        # Update track lengths
        for track in self.tracks:
            track.next_length = self.get_sequence_length()

        self.queue_outgoing.put("done")

    def handle_command(self, command):
        """
        Handle commands from the queue.
        """
        if not command:
            return

        if len(command) == 1 and command[0] == "quit":
            self.done_playing = True
        elif command[0] == "bpm":
            self.handle_bpm_command(command[1])
        elif command[0] == "regen":
            self.regenerate_rhythm(command[1])
        elif command[0] == "export":
            self.export_midi(command[1])
        elif command[0] == "modulate":
            self.metric_modulation()

    def get_command(self):
        """
        Get a command from the queue.
        """
        try:
            return self.queue_incoming.get(block=False)
        except:
            return None

    def start(self):
        """
        Starts the sequencer's main loop. This loop handles both incoming
        commands and correctly timing each track's events.
        """
        self.start_time = time.time()
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
