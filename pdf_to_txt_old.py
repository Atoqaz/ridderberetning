"""
For each file in the pdf folder, convert it to txt if it has not been done already.
This makes the file faster to seach through.
"""
import numpy as np
import os
from pathlib import Path
from pdfminer.layout import LAParams
from tqdm import tqdm
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

DIR = Path(__file__).parent
PDF_DIR = DIR.joinpath("Statskalender")
TXT_DIR = DIR.joinpath("Statskalender_txt")


def pdf_to_txt(filepath_pdf: Path, filepath_txt: Path, layout_settings: dict):
    text = extract_text(filepath_pdf, laparams=LAParams(**layout_settings))
    with open(filepath_txt, "w", encoding="utf-8") as txt_file:
        for line in text:
            txt_file.write(line)


def convert_pdf_folder_to_txt():
    pdf_files = os.listdir(PDF_DIR)
    txt_files = os.listdir(TXT_DIR)
    for filename in tqdm(pdf_files):
        filename_txt = filename.replace(".pdf", ".txt")
        if filename_txt not in txt_files:
            pdf_to_txt(
                filepath_pdf=PDF_DIR.joinpath(filename),
                filepath_txt=TXT_DIR.joinpath(filename_txt),
                layout_settings={"line_margin": 0.6},
            )


def main():
    convert_pdf_folder_to_txt()


if __name__ == "__main__":
    main()

