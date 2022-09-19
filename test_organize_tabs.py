from unittest import mock

import pytest

from guitarpro import parse, GPException

from organize_tabs import tune_value_to_note, get_guitar_tuning, move_tab_file, main


@pytest.fixture
def song():
    return parse('./Metallica - Some Kind Of Monster (guitar pro).gp3')


@pytest.mark.parametrize('value, expected', [(127, 'G'), (118, 'A#'), (999, '_')])
def test_tune_value_to_note(value, expected):
    assert tune_value_to_note(value) == expected


def test_get_guitar_tuning(song):
    assert get_guitar_tuning(song) == 'C G C F A D'


def test_move_tab_file_non_existent_destination_dir(tmp_path):
    test_file = tmp_path / 'song.gp3'
    test_file.touch()

    assert not (tmp_path / 'dest').exists()

    move_tab_file(str(test_file), f'{tmp_path}/dest')

    assert (tmp_path / 'dest/song.gp3').exists()


def test_move_tab_file_existent_destination_dir(tmp_path):
    test_file = tmp_path / 'song.gp3'
    test_file.touch()

    dest_dir = tmp_path / 'dest'
    dest_dir.mkdir()

    move_tab_file(str(test_file), f'{tmp_path}/dest')

    assert (tmp_path / 'dest/song.gp3').exists()


def test_move_tab_file_exists(tmp_path):
    test_file = tmp_path / 'song.gp3'
    test_file.touch()

    dest_dir = tmp_path / 'dest'
    dest_dir.mkdir()
    existent_file = dest_dir / 'song.gp3'
    existent_file.touch()

    with mock.patch('organize_tabs._new_filename', return_value='song123.gp3'):
        move_tab_file(str(test_file), f'{tmp_path}/dest')

    assert (tmp_path / 'dest/song.gp3').exists()
    assert (tmp_path / 'dest/song123.gp3').exists()


def test_main_ok(tmp_path):
    folder = tmp_path / 'source'
    folder.mkdir()
    test_file = folder / 'song.gp3'
    test_file.touch()

    with (
        mock.patch('organize_tabs.get_guitar_tuning', return_value='A B C'),
        mock.patch('organize_tabs.guitarpro.parse')
    ):
        main(str(tmp_path), str(tmp_path / 'dest'))

    assert (tmp_path / 'dest/A B C/song.gp3').exists()


def test_main_unsupported_guitar_pro_file(capsys, tmp_path):
    folder = tmp_path / 'source'
    folder.mkdir()
    test_file = folder / 'unsupported.gp3'
    test_file.touch()

    with mock.patch('organize_tabs.guitarpro.parse', side_effect=GPException):
        main(str(tmp_path), str(tmp_path / 'dest'))

    captured = capsys.readouterr()
    assert f'### This is not a supported Guitar Pro file: {test_file}' in captured.out
