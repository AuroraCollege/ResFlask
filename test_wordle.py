"""
Tests for wordle.py
Run with:  python -m pytest -v
"""

# Imports the WordList class you created to run tests on
from wordle import WordList 

# Instantiate the word_list object from the WordList() class
word_list = WordList() 


def test_load_words():
    assert len(word_list.words) > 0


def test_finds_real_word():
    assert word_list.contains("CRACK") == True


def test_rejects_fake_word():
    assert word_list.contains("XQZTV") == False


def test_ignores_case():
    assert word_list.contains("crack") == True


def test_random_word_is_in_list():
    assert word_list.random_word() in word_list.words


# YOUR TURN: write a test for a 4-letter word, e.g. "CATS"
