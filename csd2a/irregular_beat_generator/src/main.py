"""
Author:         Coen Konings
Date:           September 29, 2023
Last edited by: Coen Konings
On:             October 13, 2023

main.py:
Given a tempo in BPM, a set of audio files and a set of note durations, play a
rhythm.

TODO move interactions with sequencer to UserInterface class
TODO implement commands
"""
import threading
from sequencer import Sequencer
from markov import MarkovChain
from queue import Queue


class LiveCodingEnvironment:
    """
    Handles user input.
    """
    def __init__(self):
        """
        Initialize the live coding environment.
        """
        self.queue = Queue()
        self.sequencer = Sequencer(self.queue)
        self.markov_chain = MarkovChain()

    def handle_user_input(self, command):
        """
        Handle user input.
        """
        command = command.lower().split()

        if len(command) == 0:
            print("No command found.")
            return False
        elif command[0] == "quit":
            self.queue.put("quit")
            return True
        else:
            print("Please enter a valid command.")

        return False

    def get_user_input(self):
        """
        Get input until the user indicates they want to quit.
        """
        done = False

        while not done:
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
            self.queue.put("quit")

        play_thread.join()
        print("Bye!")


if __name__ == "__main__":
    LiveCodingEnvironment().start()
