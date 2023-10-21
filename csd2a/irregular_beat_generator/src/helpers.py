"""
Author:     Coen Konings
Date:       October 6, 2023
Edited by:  Coen Konings
On:         October 21, 2023

helpers.py:
Contains helper functions for input verification.
"""


def str_is_int_gt_zero(str):
    """
    Return true if the given string represents an integer larger than 0. Return
    false otherwise.
    """
    return str.isnumeric() and int(str) > 0


def rhythm_file_path(meter):
    """
    Generate the name of the appropriate rhythm file for the given meter.
    """
    return "{}_{}.txt".format(meter[0], meter[1])


if __name__ == "__main__":
    print("Please run from main.py")
