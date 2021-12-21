from time import time, perf_counter
from timeit import timeit

# start = time()

import numpy as np
from pathlib import Path

DIR = Path(__file__).parent

import re

# filename = DIR.joinpath("Statskalender/Statskalender 1950-pages-100.pdf")
# filename = DIR.joinpath("test/txt_vars_line_0.6.txt")
filename = DIR.joinpath("test/txt_vars_line_0.6.txt")


with open(filename, "r", encoding="utf-8") as file:
    count = 0
    for line in file:
        result = bool(
            re.search("^[\d\s]+.\s", line)
        )  # xxx # exception if "1.),"" Total 43 correct
        # result = bool(re.search("^—\s", line))  # Line
        # result = bool(re.search("[.][\\n]$", line))  # dot
        if result:
            count += 1
            print(line)

print(count)


sentences = [
    "29.  1. 29. Hansen, Hans Frederik Valdemar, (D.M.11/i239),Skibsinspektør* under Grønlands Styrelse.",
    "30. ",
    "— Bunding, Elias, (Fi.H.R.31.), (N.St.O.31.), ",
    "(S.V.31), Direktør, Kbhvn.",
    "Hjørring.",
    " 25.\n — ",
    "Troéls-Smith, Paul Martin, (H.T.H.), (S.",
    "Kr.3.), Kaptajn*.\n",
    "Godsejer, Eskær.",
]

# for sentence in sentences:
#     # result = re.search("^[\d]+[.][\s]", sentence)  # xxx
#     result = re.findall("[\d]+[.][\s]", sentence)  # xxx all
#     # result = re.search("^(â€”)[\s]", sentence)  # Line (Hyphen)
#     # result = re.search("[\.][\\n]$", sentence)  # dot
#     print(result)

