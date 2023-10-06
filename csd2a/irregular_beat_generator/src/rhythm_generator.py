"""
Author:         Coen Konings
Date:           September 29, 2023

Last edited by: Coen Konings
On:             October 6, 2023

main.py:
Play a default example rhythm on the sequencer in main.py.

NOTE: For this program to work, three audio files should be present in
../assets. These files should be called kick.wav, snare.wav and hat.wav.
"""
from sequencer import Sequencer
import simpleaudio as sa
from random import random


class RhythmGenerator:
    """
    A class to be used to generate rhythms.
    TODO implement.
    """
    pass


def generate_high_pattern(sequencer, length):
    """
    Generate a hihat pattern. The hihat pattern is mostly random.
    """
    audio_file = sa.WaveObject.from_wave_file("../assets/hat.wav")
    track = sequencer.add_track(length, audio_file, "kick")

    for i in range(16):
        if random() < 0.75:
            track.add_note(i, 1, 100)


def generate_mid_pattern(sequencer, length):
    """
    Generate a snare pattern. Each measure contains at least one snare that is
    played on the 2nd or 4th beat, and has a 50% chance to containe one snare
    that is played a sixteenth note early.
    """
    audio_file = sa.WaveObject.from_wave_file("../assets/snare.wav")
    track = sequencer.add_track(length, audio_file, "snare")
    offset_snare_present = False

    for i in range(16):
        if i == 5 or i == 13:
            j = i if random() < 0.5 and not offset_snare_present else i - 1
            track.add_note(j, 1, 100)


def generate_low_pattern(sequencer, length):
    """
    Generate a kick pattern. A kick is always played on the first sixteenth of
    a measure.
    """
    audio_file = sa.WaveObject.from_wave_file("../assets/kick.wav")
    track = sequencer.add_track(length, audio_file, "kick")

    for i in range(16):
        if i == 0 or random() < 0.2:
            track.add_note(i, 1, 100)


def main():
    """
    Generate a random rhythm and play it until the user wants to stop playing.
    """
    sequencer = Sequencer()
    sequencer.set_bpm(random() * 60 + 70)
    generate_low_pattern(sequencer, 16)
    generate_mid_pattern(sequencer, 16)
    generate_high_pattern(sequencer, 13)
    sequencer.start()


if __name__ == "__main__":
    main()
