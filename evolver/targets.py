from __future__ import annotations


def process_data_baseline(data: list[int]) -> int:
    total = 0
    for value in data:
        total += value * value
    return total


def process_data_listcomp(data: list[int]) -> int:
    return sum([value * value for value in data])


def process_data_generator(data: list[int]) -> int:
    return sum(value * value for value in data)
