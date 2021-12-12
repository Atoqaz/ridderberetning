import numpy as np
import pandas as pd
from pathlib import Path
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_text, extract_pages


DIR = Path(__file__).parent

# filename = DIR.joinpath("Statskalender/Statskalender 1950.pdf")
filename = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
filename = DIR.joinpath("Statskalender/sample.pdf")


location = np.array([[1, 2, 3], [4, 5, 6]])

test = np.append(location, [[7, 8, 9]], axis=0)
print(test)

