import json

import pytest

from high_score import load_high_score, save_high_score

# tmp_path is a pytest fixture: a fresh, empty folder for each test.


def test_no_file_yet_means_a_high_score_of_zero(tmp_path):
    assert load_high_score(tmp_path / "high_score.json") == 0


def test_a_saved_high_score_loads_back(tmp_path):
    path = tmp_path / "high_score.json"

    save_high_score(path, 1230)

    assert load_high_score(path) == 1230


def test_saving_again_replaces_the_old_score(tmp_path):
    path = tmp_path / "high_score.json"
    save_high_score(path, 500)

    save_high_score(path, 900)

    assert load_high_score(path) == 900


def test_the_file_is_plain_json(tmp_path):
    path = tmp_path / "high_score.json"

    save_high_score(path, 1230)

    assert json.loads(path.read_text()) == {"high_score": 1230}


def test_saving_leaves_no_temporary_files_behind(tmp_path):
    save_high_score(tmp_path / "high_score.json", 1230)

    assert [p.name for p in tmp_path.iterdir()] == ["high_score.json"]


@pytest.mark.parametrize(
    "contents",
    [
        "",  # empty file
        "{not json",  # broken JSON
        "[1, 2, 3]",  # JSON, but not an object
        "{}",  # no high_score key
        '{"high_score": "lots"}',  # not a number
        '{"high_score": 12.5}',  # not a whole number
        '{"high_score": -5}',  # negative
        '{"high_score": true}',  # a bool is an int in Python; reject it
    ],
)
def test_a_damaged_file_means_zero_instead_of_a_crash(tmp_path, contents):
    path = tmp_path / "high_score.json"
    path.write_text(contents)

    assert load_high_score(path) == 0


def test_a_file_that_is_not_text_means_zero(tmp_path):
    path = tmp_path / "high_score.json"
    path.write_bytes(b"\xff\xfe\x00garbage")

    assert load_high_score(path) == 0
