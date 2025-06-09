# test_words_finder.py
import pytest
from unittest.mock import patch, MagicMock
from WordsFinder import countExtremismWords, countThreatWords, spliter

def test_spliter():
    text = "word1 word2 word3 word4 word5 word6 word7"
    result = spliter(text, 2)
    assert len(result) == 3
    assert result[0] == "word1 word2"

def test_count_extremism_words():
    test_text = "This is a test with extremist word1 and word2"
    with patch('builtins.open', unittest.mock.mock_open(read_data="word1\nword2\nword3")):
        count = countExtremismWords(test_text)
        assert count == 2

def test_count_threat_words():
    test_text = "This is a threat with danger word1 and word2"
    with patch('builtins.open', unittest.mock.mock_open(read_data="danger\nthreat\nviolence")):
        count = countThreatWords(test_text)
        assert count == 2

@patch('tensorflow.keras.models.load_model')
@patch('pickle.load')
def test_words_search(mock_pickle, mock_model):
    mock_model.return_value.predict.return_value = [[0.99]]
    mock_pickle.return_value.texts_to_sequences.return_value = [[1, 2, 3]]
    
    from WordsFinder import WordsSearch
    result = WordsSearch(["test post with bad word"], 0, 0, -1)
    assert len(result) == 2