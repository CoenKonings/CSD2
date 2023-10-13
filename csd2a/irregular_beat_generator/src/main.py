"""
Author:         Coen Konings
Date:           September 29, 2023
Last edited by: Coen Konings
On:             October 6, 2023

main.py:
Given a tempo in BPM, a set of audio files and a set of note durations, play a
rhythm.

TODO implement UserInterface class
TODO move interactions with sequencer to UserInterface class
TODO implement commands
"""
from sequencer import Sequencer
from markov import MarkovChain


class LiveCodingEnvironment:
    """
    Handles user input.
    """
    def __init__(self):
        """
        Initialize the live coding environment.
        """
        self.sequencer = Sequencer()
        self.markov_chain = MarkovChain()

    def get_user_input(self):
        """
        Get input from the user.
        """
        return input("> ")

    def handle_user_input(self, command):
        """
        Handle user input.
        """
        command = command.split()

        if len(command) == 0:
            print("Nothing.")
            return False
        elif command[0] == "quit":
            print("Bye!")
            return True
        else:
            print("Please enter a valid command.")

        return False

    def start(self):
        """
        Start the user input loop and rhythm thread.
        TODO: threading
        """
        done = False

        while not done:
            user_input = self.get_user_input()
            done = self.handle_user_input(user_input)


if __name__ == "__main__":
    LiveCodingEnvironment().start()
