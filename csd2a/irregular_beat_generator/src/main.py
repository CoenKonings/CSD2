"""
Author:         Coen Konings
Date:           September 29, 2023
Last edited by: Coen Konings
On:             October 13, 2023

main.py:
Given a tempo in BPM, a set of audio files and a set of note durations, play a
rhythm.

TODO implement bpm command
TODO implement help command
TODO implement regen command
TODO implement export command
TODO implement modulate command
"""
import threading
import time
from sequencer import Sequencer
from markov import MarkovChain
from queue import Queue
from helpers import str_is_int_gt_zero


class LiveCodingEnvironment:
    """
    Handles user input.
    """

    def __init__(self):
        """
        Initialize the live coding environment.
        """
        self.queue_outgoing = Queue()
        self.queue_incoming = Queue()
        self.sequencer = Sequencer(self.queue_outgoing, self.queue_incoming)
        self.markov_chain = MarkovChain()

    def wait_for_sequencer(self):
        """
        Wait until the sequencer is done processing a command.
        """
        self.queue_incoming.get()

    def handle_bpm_command(self, bpm):
        """
        Set the sequencer's tempo.
        """
        self.queue_outgoing.put(("bpm", bpm))

    def handle_user_input(self, command):
        """
        Handle user input.
        TODO split validation and handling.
        """
        command = command.lower().split()

        if len(command) == 0:
            print("Please enter a command.")
        elif command[0] == "quit":
            self.queue_outgoing.put(("quit",))
            return True
        elif command[0] == "bpm" and len(command) == 2 and str_is_int_gt_zero(command[1]):
            self.handle_bpm_command(int(command[1]))
            self.wait_for_sequencer()
        else:
            print("Please enter a valid command.")

        return False

    def get_user_input(self):
        """
        Get input until the user indicates they want to quit.
        """
        done = False

        while not done:
            print(self.sequencer)
            user_input = input(">")
            done = self.handle_user_input(user_input)

    def start(self):
        """
        Start the user input loop and rhythm playing thread.
        """
        play_thread = threading.Thread(target=self.sequencer.start)

        # Ensure the play thread is stopped if the user interrupts the main
        # thread.
        try:
            play_thread.start()
            self.get_user_input()
        except KeyboardInterrupt:
            self.queue_outgoing.put("quit")

        play_thread.join()
        print("Bye!")


if __name__ == "__main__":
    LiveCodingEnvironment().start()
