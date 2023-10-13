# Irregular beat generator
Generate a beat given a user defined meter. Continue playing the rhythm while allowing the user to enter commands to change the rhythm or export it to MIDI.

## Usage
Run `python main.py` from `../src` for the CLI.

The following commands can be used to interact with the system:
- (TODO) `set <meter>`, where `<meter>` can be `5/4` or `7/8`: set the current meter. Does not change the currently playing rhythm.
- (TODO) `export <path>`: export the rhythm that's currently playing to the given midi file.
- (TODO) `regen <part>`, where `<part>` can be `high`, `mid`, `low` or `all`: generate a new rhythm in the current meter for the given part.
- (TODO) `modulate`: Change the rhythm from a 5/4 to a 7/8 feel, or conversely.
- `quit`: stop the program.
