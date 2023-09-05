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


def user_input():
    """
    Get a positive whole number from the user.
    """
    n = "-1"

    while not (n.isnumeric() and int(n) >= 0):
        n = input("How many times should the sound be played? (enter a positive integer)\n> ")

    return int(n)


def main():
    """
    Ask user how often a sound should be played and play the sound a given
    number of times.
    """
    n = user_input()
    play_sound_n_times(n)


if __name__ == "__main__":
    main()
