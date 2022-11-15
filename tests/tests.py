import os
import requests
import pytest
import requests_mock
from tests import FIXTURES_PATH
from matrix_parse.main import parse_matrix, matrix_walker, get_matrix
import json
import asyncio

EXPECTED_OUTPUT_M4X4 = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

EXPECTED_OUTPUT_M5X3 = [
    50, 90, 130, 140, 150,
    160, 170, 180, 190, 80,
    70, 60, 100, 110, 120
]

EXPECTED_OUTPUT_M6X6 = [
    1, 2, 3, 4, 5, 6,
    7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18,
    19, 20, 21, 22, 23, 24,
    25, 26, 27, 28, 29, 30,
    31, 32, 33, 34, 35, 36
]


@pytest.mark.parametrize(
    "fixture,matrix_data_path",
    [
        ("matrix_4x4.txt", 'matrix_data_4x4.json'),
        ("matrix_5x3.txt", 'matrix_data_5x3.json'),
        ('matrix_6x6.txt', 'matrix_data_6x6.json')
    ],
)
def test_parse_matrix(fixture, matrix_data_path):
    with requests_mock.Mocker() as mocker:
        with open(os.path.join(FIXTURES_PATH, fixture)) as fixture:
            mocker.get('https://fix.ture', text=fixture.read())

        content = requests.get('https://fix.ture').text

    with open(os.path.join(FIXTURES_PATH, matrix_data_path)) as matrix_data:
        assert parse_matrix(content) == json.load(matrix_data)


@pytest.mark.parametrize(
    "matrix_data_path,expected_output",
    [
        (
                'matrix_data_4x4.json',
                EXPECTED_OUTPUT_M4X4,
        ),
        (
                'matrix_data_5x3.json',
                EXPECTED_OUTPUT_M5X3,
        ),
        (
                'matrix_data_6x6.json',
                EXPECTED_OUTPUT_M6X6,
        )
    ],
)
def test_matrix_walker(matrix_data_path: dict, expected_output):
    with open(os.path.join(FIXTURES_PATH, matrix_data_path)) as matrix_data:
        assert matrix_walker(json.load(matrix_data)) == expected_output
