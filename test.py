from time import time, perf_counter
from timeit import timeit

# start = time()

import numpy as np
from pathlib import Path

DIR = Path(__file__).parent

import re

# filename = DIR.joinpath("Statskalender/Statskalender 1950-pages-100.pdf")
# filename = DIR.joinpath("test/txt_vars_line_0.6.txt")
# filename = DIR.joinpath("test/txt_vars_line_0.6.txt")


# with open(filename) as file:
#     for line in file:
#         # result = bool(re.match("^[\d]+[.][\s]", line))  # xxx
#         # result = bool(re.match("^[—][\s]", line))  # Line
#         result = bool(re.match("[.]$", line))  # dot
#         if result:
#             print(line)


# html = HTMLConverter(filename,)
# print(html)

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

for sentence in sentences:
    # result = bool(re.match("^[\d]+[.][\s]", sentence))  # xxx
    # result = bool(re.match("^[—][\s]", sentence))  # Line
    result = re.match("[\.]$", sentence)  # dot
    print(result)

