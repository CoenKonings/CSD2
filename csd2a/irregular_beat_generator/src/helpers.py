"""
Author:     Coen Konings
Date:       October 6, 2023

helpers.py:
Contains helper functions for input verification.
"""


def str_is_int_gt_zero(str):
    """
    Return true if the given string represents an integer larger than 0. Return
    false otherwise.
    """
    return str.isnumeric() and int(str) > 0


def durations_to_timestamps_16th(durations):
    """
    Given a list of durations where 1 is a quarter note, 0.5 is an eighth, etc.
    calculate a list of timestamps.
    """
    total = 0
    timestamps = []

    for duration in durations:
        timestamps.append(total)
        total += duration * 4

    return timestamps


def note_duration_valid(duration):
    """
    Check if the given string represents a valid float greater than 0.
    """
    try:
        duration = float(duration)
    except:
        return False

    if duration <= 0:
        return False

    return True


if __name__ == "__main__":
    print("Please run from main.py")
