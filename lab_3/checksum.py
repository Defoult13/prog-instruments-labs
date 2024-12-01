import csv
import hashlib
import json
import re
from typing import Any, Dict, List

import chardet


patterns: Dict[str, str] = {
    'email': r'^[^@\s]+@[^@\s]+\.[^@\s]+$',
    'height': r'^"?\d+(\.\d+)?"?$',
    'snils': r'^"?\d{11}"?$',
    'passport': r'^"?\d{2}\s\d{2}\s\d{6}"?$',
    'occupation': r'^.+$',
    'longitude': r'^-?\d+(\.\d+)?$',
    'hex_color': r'^#(?:[0-9a-fA-F]{3}){1,2}$',
    'issn': r'^\d{4}-\d{4}$',
    'locale_code': r'^[a-z]{2}-[a-z]{2}$',
    'time': r'^\d{2}:\d{2}:\d{2}(\.\d+)?$'
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
            print(f"Row {row_number}, Field '{field_name}':
                   Value '{value}' doesn't match the pattern.")
            return True
    return False

def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    ВНИМАНИЕ, ВАЖНО! Чтобы сумма получилась корректной, считать, что первая строка с данными csv-файла имеет номер 0
    Другими словами: В исходном csv 1я строка - заголовки столбцов, 2я и остальные - данные.
    Соответственно, считаем что у 2 строки файла номер 0, у 3й - номер 1 и так далее.

    Надеюсь, я расписал это максимально подробно.
    Хотя что-то мне подсказывает, что обязательно найдется человек, у которого с этим возникнут проблемы.
    Которому я отвечу, что все написано в докстринге ¯\_(ツ)_/¯

    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной пишите сами.
    Вам нужно заполнить данными - номером варианта и контрольной суммой - файл, лежащий в папке с лабораторной.
    Файл называется, очевидно, result.json.

    ВНИМАНИЕ, ВАЖНО! На json натравлен github action, который проверяет корректность выполнения лабораторной.
    Так что не перемещайте, не переименовывайте и не изменяйте его структуру, если планируете успешно сдать лабу.

    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    pass


if __name__ == "__main__":
    print(calculate_checksum([1, 2, 3]))
    print(calculate_checksum([3, 2, 1]))
