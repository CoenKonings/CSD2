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

    def wait_for_sequencer(self):
        """
        Wait until the sequencer is done processing a command.
        """
        self.queue_incoming.get()

    def handle_command_with_wait(self, command):
        """
        Send a command to the sequencer and wait until it is done.
        """
        self.queue_outgoing.put(command)
        self.wait_for_sequencer()

    def handle_command(self, command):
        """
        Have the sequencer regenerate one or all of its tracks.
        """
        self.queue_outgoing.put(command)

    def handle_user_input(self, command):
        """
        Handle user input.
        TODO split validation and handling.
        TODO send command as array?
        """
        command = command.lower().split()

        if len(command) == 0:
            print("Please enter a command.")
        elif command[0] == "quit":
            self.handle_command(command)
            return True
        elif command[0] == "bpm" and len(command) == 2 and str_is_int_gt_zero(command[1]):
            self.handle_command_with_wait(("bpm", int(command[1])))
        elif command[0] == "regen" and len(command) == 2 and command[1] in ["low", "mid", "high", "all"]:
            self.handle_command((command[0], command[1]))
        elif command[0] == "export" and len(command) == 2:
            self.handle_command((command[0], command[1]))
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
