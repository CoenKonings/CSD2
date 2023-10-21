"""
Author:         Coen Konings
Date:           September 29, 2023
Last edited by: Coen Konings
On:             October 21, 2023

main.py:
Given a tempo in BPM, a set of audio files and a set of note durations, play a
rhythm.
"""
import threading
import time
from sequencer import Sequencer
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

    def print_help(self):
        """
        Print all possible commands and a short description of their usage.
        """
        help_string = """
        quit - Quits the program
        bpm <tempo> - Sets the tempo to the given tempo in bpm. <tempo> should be a positive integer.
        regen <track> - Regenerates the rhythm for the given track. <track> should be "high", "mid", "low" or "all".
        export <filename> - Export the currently playing rhythm to a MIDI file.
        modulate - Modulate the meter from 7/8 to 5/4 or vice versa.
        help - Prints this list of commands.
        """

        print(help_string)

    def input_valid(self, command):
        """
        Validate user input. Return True if input is valid, False otherwise.
        """
        command = command.lower().split()

        if len(command) == 0:
            print("Please enter a command.")
            return False

        if command[0] not in ["quit", "bpm", "regen", "export", "modulate", "help"]:
            print("Please enter a valid command.")
            return False

        if command[0] in ["quit", "modulate", "help"] and len(command) != 1:
            print("This command does not take any parameters.")
            return False

        if command[0] in ["bpm", "regen", "export"] and len(command) != 2:
            print("Please enter exactly one parameter.")
            return False

        if command[0] == "bpm" and not str_is_int_gt_zero(command[1]):
            print("Please enter a valid BPM.")
            return False

        if command[0] == "regen" and command[1] not in ["high", "mid", "low", "all"]:
            print("Please enter a valid track to regenerate.")
            return False

        return True

    def handle_user_input(self, command):
        """
        Handle user input.
        """
        command = command.lower().split()

        if command[0] == "quit":
            self.handle_command((command[0],))
            return True
        elif command[0] == "bpm":
            self.handle_command_with_wait(("bpm", int(command[1])))
        elif command[0] == "regen":
            self.handle_command((command[0], command[1]))
        elif command[0] == "export":
            self.handle_command((command[0], command[1]))
        elif command[0] == "modulate":
            self.handle_command_with_wait((command[0],))
        elif command[0] == "help":
            self.print_help()

        return False

    def get_user_input(self):
        """
        Get input until the user indicates they want to quit.
        """
        done = False

        while not done:
            print(self.sequencer)
            user_input = input(">")

            if self.input_valid(user_input):
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
