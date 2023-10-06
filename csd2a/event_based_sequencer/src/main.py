"""
Author:         Coen Konings
Date:           September 29, 2023
Last edited by: Coen Konings
On:             October 3, 2023

main.py:
Given a tempo in BPM, a set of audio files and a set of note durations, play a
rhythm.
"""
from sequencer import Sequencer


def main():
    """
    Play a rhythm defined by the user.
    """
    sequencer = Sequencer()
    sequencer.bpm_input()
    sequencer.notes_input()
    sequencer.start()


if __name__ == "__main__":
    main()
