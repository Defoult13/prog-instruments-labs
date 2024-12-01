import csv
import hashlib
import json
import re
from typing import Any, Dict, List

import chardet


patterns: Dict[str, str] = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'height': r'^[0-2]\.\d{2}$',
    'snils': r'^\d{11}$',
    'passport': r'^\d{2} \d{2} \d{6}$',
    'occupation': r'[a-zA-Zа-яА-ЯёЁ -]+',
    'longitude': r'^\-?(180|1[0-7][0-9]|\d{1,2})\.\d+$',
    'hex_color': r'^#[A-Fa-f0-9]{6}$',
    'issn': r'^\d{4}\-\d{4}$',
    'locale_code': r'^[a-zA-Z]+(-[a-zA-Z]+)*$',
    'time': r'^\d{2}:\d{2}:\d{2}\.\d{6}$'
}


def check_row_patterns(row: List[str], row_number: int) -> bool:
    """
    Checks a string for compliance with the patterns.

    :param row: List of row values.
    :param row_number: Row number in the CSV file.
    :return: True if an error was found, False otherwise.
    """
    for i, value in enumerate(row):
        field_name = list(patterns.keys())[i]
        if not re.match(patterns[field_name], value):
            return True
    return False


def determine_encoding(file_path: str) -> str:
    """
    Defines the file encoding.

    :param file_path: Path to the file.
    :return: File encoding.
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        return encoding
    except Exception as e:
        print(f"Error in determining the encoding of the file {file_path}: {e}")
        raise


def process_csv(file_path: str) -> List[int]:
    """
    Processes a CSV file and returns line numbers with errors.

    :param file_path: Path to the CSV file.
    :return: List of line numbers with errors.
    """
    invalid_rows: List[int] = []
    try:
        encoding = determine_encoding(file_path)
        with open(file_path, newline='', encoding=encoding) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader)
            for row_number, row in enumerate(reader):
                if check_row_patterns(row, row_number):
                    invalid_rows.append(row_number)
    except FileNotFoundError:
        print(f"The file was not found: {file_path}")
    except Exception as e:
        print(f"Error reading the file: {e}")
    return invalid_rows


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Calculates checksum for list of string's number

    :param row_numbers: list of integer row numbers of the csv file where validation errors were found
    :return: md5 hash for checking via github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Serializes result in JSON file

    :param variant: your variant number
    :param checksum: checksum calculated via calculate_checksum()
    """
    try:
        with open('lab_3/result.json', 'r', encoding='utf-8') as json_file:
            result_data: Dict[str, Any] = json.load(json_file)
    except OSError as er: 
        raise OSError(f"Error occured during serializing the result: {er}")

    result_data['checksum'] = checksum
    with open('lab_3/result.json', 'w', encoding='utf-8') as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    try:
        with open("lab_3/config.json", "r", encoding='utf-8') as config_file:
            config = json.load(config_file)

        invalid_row_numbers = process_csv(config["csv_path"])
        checksum = calculate_checksum(invalid_row_numbers)
        var = 51
        serialize_result(var, checksum)

    except FileNotFoundError:
        print("The file config.json was not found.")
    except Exception as e:
        print(f"Error: {e}")
