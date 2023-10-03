"""
Author:         Coen Konings
Date:           September 29, 2023
Last edited by: Coen Konings
On:             October 3, 2023

main.py:
Play a default example rhythm on the sequencer in main.py.

NOTE: For this program to work, three audio files should be present in
../assets. These files should be called kick.wav, snare.wav and hat.wav.
"""
from main import start_play_thread
from sequencer import NoteEvent
import simpleaudio as sa
from random import random


def generate_hat_pattern():
    """
    Generate a hihat pattern. The hihat pattern is mostly random.
    """
    audio_file = sa.WaveObject.from_wave_file("../assets/hat.wav")
    note_events = []

    for i in range(16):
        if random() < 0.75 or i == 15:
            note_events.append(NoteEvent(i, audio_file, 1, 100))

    return note_events


def generate_snare_pattern():
    """
    Generate a snare pattern. Each measure contains at least one snare that is
    played on the 2nd or 4th beat, and has a 50% chance to containe one snare
    that is played a sixteenth note early.
    """
    audio_file = sa.WaveObject.from_wave_file("../assets/snare.wav")
    note_events = []
    offset_snare_present = False

    for i in range(16):
        if i == 5 or i == 13:
            j = i if random() < 0.5 and not offset_snare_present else i - 1
            note_events.append(NoteEvent(j, audio_file, 1, 100))

    return note_events


def generate_kick_pattern():
    """
    Generate a kick pattern. A kick is always played on the first sixteenth of
    a measure.
    """
    audio_file = sa.WaveObject.from_wave_file("../assets/kick.wav")
    note_events = []

    for i in range(16):
        if i == 0 or random() < 0.2:
            note_events.append(NoteEvent(i, audio_file, 1, 100))

    return note_events


def main():
    """
    Generate a random rhythm and play it until the user wants to stop playing.
    """
    note_events = generate_kick_pattern() + generate_snare_pattern() + generate_hat_pattern()
    note_events.sort()
    bpm = random() * 60 + 70
    start_play_thread(note_events, bpm)


if __name__ == "__main__":
    main()
