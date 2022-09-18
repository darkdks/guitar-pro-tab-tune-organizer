from fileinput import filename
import os
import fnmatch
import guitarpro
import shutil
import random

value_note_list = [
    {"value": 127, "note": "G9"},
    {"value": 126, "note": "F#"},
    {"value": 125, "note": "F9"},
    {"value": 124, "note": "E9"},
    {"value": 123, "note": "D#"},
    {"value": 122, "note": "D9"},
    {"value": 121, "note": "C#"},
    {"value": 120, "note": "C9"},
    {"value": 119, "note": "B8"},
    {"value": 118, "note": "A#"},
    {"value": 117, "note": "A8"},
    {"value": 116, "note": "G#"},
    {"value": 115, "note": "G8"},
    {"value": 114, "note": "F#"},
    {"value": 113, "note": "F8"},
    {"value": 112, "note": "E8"},
    {"value": 111, "note": "D#"},
    {"value": 110, "note": "D8"},
    {"value": 109, "note": "C#"},
    {"value": 108, "note": "C8"},
    {"value": 107, "note": "B7"},
    {"value": 106, "note": "A#"},
    {"value": 105, "note": "A7"},
    {"value": 104, "note": "G#"},
    {"value": 103, "note": "G7"},
    {"value": 102, "note": "F#"},
    {"value": 101, "note": "F7"},
    {"value": 100, "note": "E7"},
    {"value": 99, "note": "D#"},
    {"value": 98, "note": "D7"},
    {"value": 97, "note": "C#"},
    {"value": 96, "note": "C7"},
    {"value": 95, "note": "B6"},
    {"value": 94, "note": "A#"},
    {"value": 93, "note": "A6"},
    {"value": 92, "note": "G#"},
    {"value": 91, "note": "G6"},
    {"value": 90, "note": "F#"},
    {"value": 89, "note": "F6"},
    {"value": 88, "note": "E6"},
    {"value": 87, "note": "D#"},
    {"value": 86, "note": "D6"},
    {"value": 85, "note": "C#"},
    {"value": 84, "note": "C6"},
    {"value": 83, "note": "B5"},
    {"value": 82, "note": "A#"},
    {"value": 81, "note": "A5"},
    {"value": 80, "note": "G#"},
    {"value": 79, "note": "G5"},
    {"value": 78, "note": "F#"},
    {"value": 77, "note": "F5"},
    {"value": 76, "note": "E5"},
    {"value": 75, "note": "D#"},
    {"value": 74, "note": "D5"},
    {"value": 73, "note": "C#"},
    {"value": 72, "note": "C5"},
    {"value": 71, "note": "B4"},
    {"value": 70, "note": "A#"},
    {"value": 69, "note": "A4"},
    {"value": 68, "note": "G#"},
    {"value": 67, "note": "G4"},
    {"value": 66, "note": "F#"},
    {"value": 65, "note": "F4"},
    {"value": 64, "note": "E4"},
    {"value": 63, "note": "D#"},
    {"value": 62, "note": "D4"},
    {"value": 61, "note": "C#"},
    {"value": 60, "note": "C4"},
    {"value": 59, "note": "B3"},
    {"value": 58, "note": "A#"},
    {"value": 57, "note": "A3"},
    {"value": 56, "note": "G#"},
    {"value": 55, "note": "G3"},
    {"value": 54, "note": "F#"},
    {"value": 53, "note": "F3"},
    {"value": 52, "note": "E3"},
    {"value": 51, "note": "D#"},
    {"value": 50, "note": "D3"},
    {"value": 49, "note": "C#"},
    {"value": 48, "note": "C3"},
    {"value": 47, "note": "B2"},
    {"value": 46, "note": "A#"},
    {"value": 45, "note": "A2"},
    {"value": 44, "note": "G#"},
    {"value": 43, "note": "G2"},
    {"value": 42, "note": "F#"},
    {"value": 41, "note": "F2"},
    {"value": 40, "note": "E2"},
    {"value": 39, "note": "D#"},
    {"value": 38, "note": "D2"},
    {"value": 37, "note": "C#"},
    {"value": 36, "note": "C2"},
    {"value": 35, "note": "B1"},
    {"value": 34, "note": "A#"},
    {"value": 33, "note": "A1"},
    {"value": 32, "note": "G#"},
    {"value": 31, "note": "G1"},
    {"value": 30, "note": "F#"},
    {"value": 29, "note": "F1"},
    {"value": 28, "note": "E1"},
    {"value": 27, "note": "D#"},
    {"value": 26, "note": "D1"},
    {"value": 25, "note": "C#"},
    {"value": 24, "note": "C1"},
    {"value": 23, "note": "B0"},
    {"value": 22, "note": "A#"},
    {"value": 21, "note": "A0"}]


def main(source, destination):
    print("Filtering...\n")
    supported_extensions = '*.gp[345]'

    for dirpath, dirs, files in os.walk(source):
        for file in fnmatch.filter(files, supported_extensions):
            guitar_pro_path = os.path.join(dirpath, file)
            try:
                tab = guitarpro.parse(guitar_pro_path)
            except guitarpro.GPException as exc:
                print("###This is not a supported Guitar Pro file:", guitar_pro_path, ":", exc)
            else:
                guitar_tuning = getGuitarTuning(tab)
                print('\nTab', ':', os.path.basename(guitar_pro_path), 'Tunning', ':', ' '.join(guitar_tuning))
                try:
                    moveFile(guitar_pro_path, os.path.join(destination, ' '.join(guitar_tuning)))
                except:
                    print('Falied to move tab')
    print("\nDone!")


def getGuitarTuning(tab):
    guitar_tune = []
    for track in tab.tracks:
        if not track.isPercussionTrack and len(track.strings) > 5:
            for string in track.strings:
                guitar_tune.append(tuneValueToNote(string.value, True))
            break

    guitar_tune.reverse()
    return guitar_tune


def tuneValueToNote(value, shortWay):
    for value_note in value_note_list:
        if value_note["value"] == value:
            if shortWay and value_note["note"][1].isdigit():
                return value_note["note"][0]
            else:
                return value_note["note"]
    return "_"


def moveFile(sourcePath, destinationDir):
    file_name = os.path.basename(sourcePath)
    dest_path = os.path.join(destinationDir, file_name)

    if os.path.normpath(sourcePath) == os.path.normpath(dest_path):
        return print(f'Ignoring {destinationDir} because the source and destination is the same')

    if not os.path.exists(destinationDir):
        os.makedirs(destinationDir)
        
    if os.path.exists(dest_path):
        new_file_name = os.path.splitext(file_name)[0] + str(random.randint(0, 100000)) + os.path.splitext(file_name)[1]   
        os.rename(sourcePath, os.path.join(os.path.dirname(sourcePath), new_file_name))
        shutil.move(os.path.join(os.path.dirname(sourcePath), new_file_name), destinationDir)         
        print(f'Moving Tab {os.path.basename(sourcePath)} to {new_file_name}')
    else:
        shutil.move(sourcePath, destinationDir)


if __name__ == '__main__':
    import argparse
    description = ("Just a small script to check all the tabs in a folder and move them to another directory according to the guitar tuning.")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('source',
                        metavar='SOURCE',
                        help='path to the source tabs folder')

    parser.add_argument('destination',
                        metavar='DESTINATION',
                        help='path to the destination tabs folder')

    args = parser.parse_args()
    kwargs = dict(args._get_kwargs())
    print(kwargs)
    main(**kwargs)
