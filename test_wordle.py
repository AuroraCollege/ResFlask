"""
Tests for wordle.py
Run with:  python -m pytest -v
"""

from wordle import WordList
word_list = WordList("words.txt")


def test_load_words():
    assert len(word_list.words) > 0


def test_finds_real_word():
    assert word_list.contains("CRANE") == True


def test_rejects_fake_word():
    assert word_list.contains("XQZTV") == False


def test_ignores_case():
    assert word_list.contains("crane") == True


def test_random_word_is_in_list():
    assert word_list.random_word() in word_list.words


# YOUR TURN: write a test for a 4-letter word, e.g. "CATS"
