from time import time, perf_counter
from timeit import timeit

# start = time()

import numpy as np
import pandas as pd
from pathlib import Path
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.converter import HTMLConverter

DIR = Path(__file__).parent

filename = DIR.joinpath("Statskalender/Statskalender 1950-pages-100.pdf")
# filename = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
# filename = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
# filename = DIR.joinpath("test/txt_vars_line_0.6.txt")


# with open(filename) as file:
#     for line in file:
#         print(line)


# html = HTMLConverter(filename,)
# print(html)

