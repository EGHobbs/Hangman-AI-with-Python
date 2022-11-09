from project import (
    letter_position,
    get_most_frequent,
    get_letter_frequency,
    TrialWord,
    HangmanWord,
    letters_match,
    has_extra_copies,
    has_invalid_letter,
)
import pytest


def test_has_invalid_letter():
    TrialWord.known_letters.append({"letter": "t", "position": "None"})
    assert has_invalid_letter("cat") == True
    assert has_invalid_letter("dog") == False


def test_has_extra_copies():
    TrialWord.known_letters.append({"letter": "l", "position": 0})
    assert has_extra_copies("lit") == False
    assert has_extra_copies("lol") == True
    TrialWord.known_letters.clear()


def test_letters_match():
    TrialWord.known_letters.append({"letter": "t", "position": 2})
    assert letters_match(TrialWord("cat")) == True
    with pytest.raises(ValueError):
        TrialWord("ate")
    with pytest.raises(ValueError):
        TrialWord("dog")
    TrialWord.known_letters.clear()
    TrialWord.known_letters.append({"letter": "l", "position": 0})
    TrialWord.known_letters.append({"letter": "l", "position": 2})
    assert letters_match(TrialWord("lol")) == True
    with pytest.raises(ValueError):
        TrialWord("lit")
    TrialWord.known_letters.clear()


def test_letter_position():
    iter = letter_position("a", TrialWord("attach"))
    assert next(iter) == 0
    assert next(iter) == 3
    with pytest.raises(StopIteration):
        next(iter)
    with pytest.raises(StopIteration):
        next(letter_position("a", TrialWord("dog")))


def test_get_most_frequent():
    assert get_most_frequent({"a": 1, "c": 3, "z": 2}) == "c"
    assert get_most_frequent({"f": 100, "a": 54, "c": 100}) == "f"


def test_get_letter_frequency():
    assert get_letter_frequency(HangmanWord("move"), doc="testwords.txt") == {
        "o": 2
    } | {l: 1 for l in "luckrf"} | {l: 0 for l in "abdeghijmnpqstvwxyz"}
    assert get_letter_frequency(HangmanWord("cat"), doc="testwords.txt") == {
        l: 2 for l in "ad"
    } | {l: 1 for l in "bctspyre"} | {l: 0 for l in "fghijklmnoquvwxz"}
    TrialWord.known_letters.append({"letter": "o", "position": "None"})
    assert get_letter_frequency(HangmanWord("yert"), doc="testwords.txt") == {
        l: 1 for l in "luck"
    } | {l: 0 for l in "abdeghijmnpqstvwxyzrfo"}
    TrialWord.known_letters.append({"letter": "t", "position": 0})
    assert get_letter_frequency(HangmanWord("leaks"), doc="testwords.txt") == {
        l: 1 for l in "truck"
    } | {l: 0 for l in "abdefghijlmnopqsvwxyz"}
    TrialWord.known_letters.clear()
