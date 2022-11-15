from copy import deepcopy
import re
import aiohttp
import asyncio
import sys


SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'


async def get_matrix(url: str) -> list[int]:
    matrix_data = parse_matrix(await net(url))
    return matrix_walker(matrix_data)


async def net(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                assert response.status == 200
                return await response.text()
        except BaseException as err:
            print(err)
            sys.exit(1)


def parse_matrix(content_str: str) -> dict:

    try:
        assert '+-----+\n|' in content_str[:200]
    except AssertionError:
        print("Matrix doesn't exist")
        sys.exit(1)

    rows_count = len(list(filter(None, content_str.split("\n")))[1::2])
    content = re.compile(r"(?<=\s)([0-9]+)(?=\s)").findall(content_str)
    columns_count = len(content) // rows_count
    matrix = [
        [int(x) for x in content[columns_count * i: (i + 1) * columns_count]]
        for i in range(rows_count)
    ]
    return {
        "matrix": matrix,
        "columns_count": columns_count,
        "rows_count": rows_count,
    }


def matrix_walker(matrix_data: dict) -> list[int]:
    rows_count = matrix_data["rows_count"]
    columns_count = matrix_data["columns_count"]
    matrix = matrix_data["matrix"]
    fin_matrix = []
    i = 0
    x = 0
    y = -1
    d_row = 1
    d_column = 0
    while i < rows_count * columns_count:
        if (
                0 <= y + d_row < rows_count
                and 0 <= x + d_column < columns_count
                and matrix[y + d_row][x + d_column] != 0
        ):
            x += d_column
            y += d_row
            fin_matrix.append(deepcopy(matrix[y][x]))
            matrix[y][x] = 0
            i += 1
        else:
            if d_row == 1:
                d_row = 0
                d_column = 1
            elif d_column == 1:
                d_row = -1
                d_column = 0
            elif d_row == -1:
                d_row = 0
                d_column = -1
            elif d_column == -1:
                d_row = 1
                d_column = 0

    return fin_matrix


if __name__ == '__main__':
    print(asyncio.run(get_matrix(SOURCE_URL)))
