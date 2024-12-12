import pytest
import json
from unittest.mock import mock_open, patch
from NIST_test import (bit_frequency_test,
                       consecutive_bit_test, longest_run_of_ones_test)

def test_reading():
    mock_data = '{"cpp": "10110101101100010110001011101110011011111100111110000101010100010001110100111001110000011011011001011100011101110001111111000100"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        file_path = "mocked_path/gen_results.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    text = data["cpp"]
    assert text == "10110101101100010110001011101110011011111100111110000101010100010001110100111001110000011011011001011100011101110001111111000100"

def test_bit_frequency():
    sequence = "10110101101100010110001011101110011011111100111110000101010100010001110100111001110000011011011001011100011101110001111111000100"
    frequency = 0.2888443663464849
    assert frequency == bit_frequency_test(sequence)

@pytest.mark.parametrize("name, value", [("java", 0.11161176829829222)])
def test_bit_frequency_test_w_r(name, value):
    file_path = "K:/Pyth/TMP/prog-instruments-labs/lab_4/gen_results.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    sequence = data[name]
    frequency = bit_frequency_test(sequence)
    assert frequency == value

@pytest.mark.parametrize("name, value", [("java", 0.4142161782425251)])
def test_bit_frequency_test_w_r_m(name, value):
    mock_data = '{"java": "101101"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        file_path = "mocked_path/gen_results.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    sequence = data[name]
    frequency = bit_frequency_test(sequence)
    assert frequency == value

def test_consecutive_bit_test():
    sequence = "10110101101100010110001011101110011011111100111110000101010100010001110100111001110000011011011001011100011101110001111111000100"
    frequency = 0.6637700912920717
    assert frequency == consecutive_bit_test(sequence)

@pytest.mark.parametrize("name, value", [("java", 0.9617930523408253)])
def test_consecutive_bit_test_w_r(name, value):
    file_path = "K:/Pyth/TMP/prog-instruments-labs/lab_4/gen_results.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    sequence = data[name]
    frequency = consecutive_bit_test(sequence)
    assert frequency == value

@pytest.mark.parametrize("name, value", [("java", 0.22067136191984693)])
def test_consecutive_bit_test_w_r_m(name, value):
    mock_data = '{"java": "101101"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        file_path = "mocked_path/gen_results.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    sequence = data[name]
    frequency = consecutive_bit_test(sequence)
    assert frequency == value

def test_longest_run_of_ones_test():
    sequence = "10110101101100010110001011101110011011111100111110000101010100010001110100111001110000011011011001011100011101110001111111000100"
    frequency = 0.7843046841167867
    assert frequency == longest_run_of_ones_test(sequence)

@pytest.mark.parametrize("name, value", [("java", 0.39173926585761465)])
def test_longest_run_of_ones_test_w_r_m(name, value):
    file_path = "K:/Pyth/TMP/prog-instruments-labs/lab_4/gen_results.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    sequence = data[name]
    frequency = longest_run_of_ones_test(sequence)
    assert frequency == value

@pytest.mark.parametrize("name, value", [("java", 0.002682392443551449)])
def test_longest_run_of_ones_test_w_r(name, value):
    mock_data = '{"java": "101101"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        file_path = "mocked_path/gen_results.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    sequence = data[name]
    frequency = longest_run_of_ones_test(sequence)
    assert frequency == value
