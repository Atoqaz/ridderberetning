"""
For each file in the pdf folder, convert it to txt if it has not been done already.
This makes the file faster to seach through.
"""

import numpy as np
import os
from pathlib import Path
import re

# from pdfminer.layout import LAParams
from tqdm import tqdm

# from pdfminer.high_level import extract_text
# from pdfminer.layout import LAParams

DIR = Path(__file__).parent
# PDF_DIR = DIR.joinpath("Statskalender")
# TXT_DIR = DIR.joinpath("Statskalender_txt")
PDF_DIR = DIR.joinpath("test2")
TXT_DIR = DIR.joinpath("test")

import fitz


# TODO: Consider when a line ends. Maybe combine sentences when extracting them??
# sentence starting with a small letter should be the end of the previous?
def extract_text_from_pdf(filepath_pdf):
    offset_y = 5
    offset_x = 100
    with open(filepath_pdf, "rb") as file:
        text = ""
        with fitz.open(filepath_pdf) as pdf:
            page_text = ""
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                x_old, y_old = 0, 0
                # (x0, y0, x1, y1, "word", block_no, line_no, word_no)
                # https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractWORDS
                for word in page.get_text("words"):
                    x, y = word[0], word[1]

                    if (y > y_old + offset_y) and (not word[4].islower()):
                        page_text += "\n"
                    elif abs(x_old - x) <= offset_x:
                        page_text += " "

                    page_text += word[4].replace("\xad", "")

                    y_old = y
                    x_old = x
            text += page_text
            text += "\n\x0c"
    return text


def pdf_to_txt(filepath_pdf: Path, filepath_txt: Path, layout_settings: dict):

    # text = extract_text(filepath_pdf, laparams=LAParams(**layout_settings))
    print(filepath_pdf)
    text = extract_text_from_pdf(filepath_pdf)

    with open(filepath_txt, "w", encoding="utf-8") as txt_file:
        for line in text:
            txt_file.write(line)


def convert_pdf_folder_to_txt():
    pdf_files = os.listdir(PDF_DIR)
    print(pdf_files)
    # txt_files = os.listdir(TXT_DIR)
    for filename in tqdm(pdf_files):
        filename_txt = filename.replace(".pdf", ".txt")
        print(filename)
        # if filename_txt not in txt_files:
        pdf_to_txt(
            filepath_pdf=PDF_DIR.joinpath(filename),
            filepath_txt=TXT_DIR.joinpath(filename_txt),
            layout_settings={"line_margin": 0.6},
        )


def main():
    convert_pdf_folder_to_txt()


if __name__ == "__main__":
    main()
