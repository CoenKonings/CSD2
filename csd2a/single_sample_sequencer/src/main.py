import simpleaudio as sa
from time import sleep


def play_sound(duration=-1):
    """
    Play sample.wav once. Wait until playback has finished.
    """
    # From https://simpleaudio.readthedocs.io/en/latest/
    wave_obj = sa.WaveObject.from_wave_file("../samples/plokrkr.wav")
    play_obj = wave_obj.play()

    if duration >= 0:
        sleep(duration)
    else:
        play_obj.wait_done()


def play_sound_n_times(n):
    """
    Play sample.wav n times. Parameter n should be a positive integer.
    """
    for _ in range(n):
        play_sound(2)


def quarter_note_duration_from_bpm(bpm):
    """
    Given the bpm, calculate the duration of a quarter note in seconds.
    """
    return 60 / bpm


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


def get_rhythm(n_plays):
    """
    Given the number of times a sample should be played, get the duration for
    each play. Each duration is given using a number, where 1 is a quarter
    note, 0.5 is an eighth note, 0.25 is a sixteenth, etc.
    """
    rhythm = []

    while len(rhythm) < n_plays:
        duration = input("Duration for note {}, where 1 is a quarter note:\n> ".format(len(rhythm) + 1))

        if not note_duration_valid(duration):
            print("Please enter a valid positive number. Example: 1.5")
            continue

        rhythm.append(float(duration))

    return rhythm


def get_int_greater_than_zero(prompt):
    """
    Get an integer greater than 0 from the user.
    """
    user_input = "-1"

    while not (user_input.isnumeric() and int(user_input) > 0):
        user_input = input(prompt)

    return int(user_input)


def main():
    """
    Ask user how often a sound should be played and play the sound a given
    number of times.
    """
    n_plays = get_int_greater_than_zero("How many notes do you want to enter?\n> ")
    rhythm = get_rhythm(n_plays)
    bpm = get_int_greater_than_zero("At what bpm should the rhythm be played?\n> ")
    quarter = quarter_note_duration_from_bpm(bpm)


if __name__ == "__main__":
    main()
