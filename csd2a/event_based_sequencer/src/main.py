"""
Author:         Coen Konings
Date:           September 29, 2023
Last edited by: Coen Konings
On:             October 3, 2023

main.py:
Given a tempo in BPM, a set of audio files and a set of note durations, play a
rhythm.
"""
import simpleaudio as sa
from time import sleep, time
from os.path import isfile
from queue import Queue
from sequencer import Sequencer
import threading
from helpers import str_is_int_gt_zero


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


def input_while_playing(queue):
    """
    Get input from the user and send it into the queue.
    """
    while True:
        command = input(
            "Q to stop playing, or a positive integer to change the BPM.\n>"
        )

        if command.lower() == "q":
            queue.put("stop")
            break
        elif str_is_int_gt_zero(command):
            queue.put(int(command))


def start_play_thread(note_events, bpm):
    q = Queue()
    play_thread = threading.Thread(target=play_rhythm, args=[note_events, bpm, q])

    try:
        play_thread.start()
        input_while_playing(q)
    except KeyboardInterrupt:
        q.put("stop")

    play_thread.join()
    print("Bye!")


def main():
    """
    Play a rhythm defined by the user.
    """
    sequencer = Sequencer()
    sequencer.bpm_input()
    sequencer.notes_input()

    # note_events = note_events_input()
    # note_events.sort()
    # start_play_thread(note_events, bpm)


if __name__ == "__main__":
    main()
