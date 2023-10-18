# Irregular beat generator
Generate a beat given a user defined meter. Continue playing the rhythm while allowing the user to enter commands to change the rhythm or export it to MIDI.

## Requirements
See `requirements.txt` in the root folder of this repository for the required Python libraries.

The irregular beat generator expects three audio files to be present:
1. `../assets/kick.wav`,
2. `../assets/snare.wav`,
3. `../assets/hat.wav`.

Here, `kick.wav` contains the sound for the low layer of the rhythm, `snare.wav` contains the sound for the middle layer of the rhythm, and `hat.wav` contains the sound for the high layer of the rhythm.

## Usage
Run `python main.py` from `../src` for the CLI.

The following commands can be used to interact with the system:
- (TODO) `export <path>`: export the rhythm that's currently playing to the given midi file.
- (TODO) `regen <part>`, where `<part>` can be `high`, `mid`, `low` or `all`: generate a new rhythm in the current meter for the given part.
- (TODO) `modulate`: Change the rhythm from a 5/4 to a 7/8 feel, or conversely.
- `quit`: stop the program.

## Process description
The Sequencer class that was already present was restructured to accept commands from a newly created LiveCodingEnvironment class. Upon receiving the `regen` command, it uses the MarkovChain class to generate a new rhythm.

Unfortunately, the tactic for compound meter beat generation described in `PLAN.md` does not yield the best result - the beats appear somewhat erratic and the feel of the meter is not present. Because of this, beat generation will be changed to be based on adding groups of 2 or 3 sixteenth notes to the kick and snare, and a fully random pattern on the hihat.
