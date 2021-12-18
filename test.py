from time import time, perf_counter
from timeit import timeit

# start = time()

import numpy as np
import pandas as pd
from pathlib import Path
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

DIR = Path(__file__).parent

filename = DIR.joinpath("Statskalender/Statskalender 1950-pages-100.pdf")
# filename = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
# filename = DIR.joinpath("Statskalender/sample.pdf")


# # text = extract_text("Statskalender/sample.pdf")
# start = perf_counter()
# # text = extract_text("Statskalender/Statskalender 1950.pdf") # 458 sec
# text = extract_text("Statskalender/sample.pdf")

# end = perf_counter()
# print(round((end - start), 4), "sec")
# print(repr(text))
# print(text)

# sentence = '(S.N.3.), (S.V.22.), Overretssagf., Kbhvn.'
# print()
laparams = LAParams()
print(laparams)

# from pdfminer.high_level import extract_pages

# for page_layout in extract_pages(filename):
#     for element in page_layout:
#         print(element)
