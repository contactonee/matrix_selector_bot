from os import PathLike
from typing import List, Tuple, Dict

import numpy as np
import json


def knapsack(w: List[int],
             W: int) -> Tuple[List[int], int]:

    n = len(w)

    res = np.zeros((n + 1, W + 1), np.int32)

    for i in range(1, n + 1):
        for j in range(W + 1):
            if w[i - 1] > j:
                res[i][j] = res[i - 1][j]
            else:
                res[i][j] = max(res[i - 1, j],
                                res[i - 1, j - w[i-1]] + w[i-1])

    return restore_knapsack(w, res), res[-1, -1]


def restore_knapsack(w: List[int],
                     res: np.ndarray) -> List[int]:

    if res[-1, -1] == 0:
        return []
    if res[-1, -1] == res[-2, -1]:
        return restore_knapsack(w, res[:-1])
    else:
        it = w[res.shape[0] - 2]
        return [*restore_knapsack(w, res[:-1, :res[-1, -1] - it + 1]), it]


class Phrases:
    phrases: Dict[str, Dict[str, str]]
    lang: str

    def __init__(self, file: PathLike, lang=None) -> None:
        self.phrases = json.load(file)

        if lang is not None:
            self.set_lang(lang)
        else:
            self.set_lang(list(self.phrases.keys())[0])

    def set_lang(self, lang: str) -> None:
        if lang not in self.phrases:
            raise ValueError(f"{lang} is not present in phrases file")
        self.lang = lang

    def get_phrase(self, phrase: str) -> str:
        return self.phrases[self.lang][phrase]


def parse_matrices_values(text):

    values = text
    values = values.strip(' \t\n').split(',')
    values = list(map(int, map(str.strip, values)))

    return values
