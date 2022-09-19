import os
import random
from pathlib import Path

import guitarpro

VALUE_NOTE_MAP = {
    21: 'A0',
    22: 'A#',
    23: 'B0',
    24: 'C1',
    25: 'C#',
    26: 'D1',
    27: 'D#',
    28: 'E1',
    29: 'F1',
    30: 'F#',
    31: 'G1',
    32: 'G#',
    33: 'A1',
    34: 'A#',
    35: 'B1',
    36: 'C2',
    37: 'C#',
    38: 'D2',
    39: 'D#',
    40: 'E2',
    41: 'F2',
    42: 'F#',
    43: 'G2',
    44: 'G#',
    45: 'A2',
    46: 'A#',
    47: 'B2',
    48: 'C3',
    49: 'C#',
    50: 'D3',
    51: 'D#',
    52: 'E3',
    53: 'F3',
    54: 'F#',
    55: 'G3',
    56: 'G#',
    57: 'A3',
    58: 'A#',
    59: 'B3',
    60: 'C4',
    61: 'C#',
    62: 'D4',
    63: 'D#',
    64: 'E4',
    65: 'F4',
    66: 'F#',
    67: 'G4',
    68: 'G#',
    69: 'A4',
    70: 'A#',
    71: 'B4',
    72: 'C5',
    73: 'C#',
    74: 'D5',
    75: 'D#',
    76: 'E5',
    77: 'F5',
    78: 'F#',
    79: 'G5',
    80: 'G#',
    81: 'A5',
    82: 'A#',
    83: 'B5',
    84: 'C6',
    85: 'C#',
    86: 'D6',
    87: 'D#',
    88: 'E6',
    89: 'F6',
    90: 'F#',
    91: 'G6',
    92: 'G#',
    93: 'A6',
    94: 'A#',
    95: 'B6',
    96: 'C7',
    97: 'C#',
    98: 'D7',
    99: 'D#',
    100: 'E7',
    101: 'F7',
    102: 'F#',
    103: 'G7',
    104: 'G#',
    105: 'A7',
    106: 'A#',
    107: 'B7',
    108: 'C8',
    109: 'C#',
    110: 'D8',
    111: 'D#',
    112: 'E8',
    113: 'F8',
    114: 'F#',
    115: 'G8',
    116: 'G#',
    117: 'A8',
    118: 'A#',
    119: 'B8',
    120: 'C9',
    121: 'C#',
    122: 'D9',
    123: 'D#',
    124: 'E9',
    125: 'F9',
    126: 'F#',
    127: 'G9',
}


def main(source, destination):
    dest = Path(destination)

    print('Filtering...')
    for path in Path(source).glob('**/*.gp[345]'):
        try:
            tab = guitarpro.parse(path)
        except guitarpro.GPException as e:
            print(f'### This is not a supported Guitar Pro file: {path} : {e}')
        else:
            guitar_tuning = get_guitar_tuning(tab)
            try:
                move_tab_file(path, dest / guitar_tuning)
            except Exception:
                print('Falied to move tab')

    print('Done!')


def get_guitar_tuning(tab):
    guitar_tune = []
    for track in tab.tracks:
        if not track.isPercussionTrack and len(track.strings) > 5:
            guitar_tune.extend(
                tune_value_to_note(string.value)
                for string in reversed(track.strings)
            )
            break

    return ' '.join(guitar_tune)


def tune_value_to_note(value, short_way=True, default='_'):
    try:
        note = VALUE_NOTE_MAP[value]
    except KeyError:
        return default

    if short_way and note[1].isdigit():
        return note[0]

    return note


def move_tab_file(source, destination):
    source = Path(source)
    dest = Path(destination) / source.name

    if source == dest:
        print(
            f'Ignoring {destination} because the source and destination is the same'
        )
        return

    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        new_filename = _new_filename(dest)
        dest = dest.parent / new_filename

    print(f'Moving Tab from {source} to {dest}')
    source.rename(dest)


def _new_filename(filename):
    path, ext = os.path.splitext(filename)
    return f'{path}{random.randint(0, 10000)}{ext}'


def cli():
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            'Just a small script to check all the tabs in a folder and '
            'move them to another directory according to the guitar tuning.'
        )
    )
    parser.add_argument(
        'source',
        metavar='SOURCE',
        help='path to the source tabs folder',
        type=Path,
    )
    parser.add_argument(
        'destination',
        metavar='DESTINATION',
        help='path to the destination tabs folder',
        type=Path,
    )

    args = parser.parse_args()
    main(**vars(args))
    exit(0)


if __name__ == '__main__':
    cli()
