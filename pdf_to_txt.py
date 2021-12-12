"""
For each file in the pdf folder, convert it to txt if it has not been done already.
This makes the file faster to seach through.
"""

import os
from pathlib import Path
from tqdm import tqdm
from pdfminer.high_level import extract_text

DIR = Path(__file__).parent
PDF_DIR = DIR.joinpath("Statskalender")
TXT_DIR = DIR.joinpath("Statskalender_txt")


def pdf_to_txt(filepath_load: Path, filepath_save: Path):
    text = extract_text(filepath_load)
    with open(filepath_save, "w", encoding="utf-8") as txt_file:
        for line in text:
            txt_file.write(line)


def main():
    pdf_files = os.listdir(PDF_DIR)
    txt_files = os.listdir(TXT_DIR)
    for filename in tqdm(pdf_files):
        filename_txt = filename.replace(".pdf", ".txt")
        if filename_txt not in txt_files:
            print(filename)
            pdf_to_txt(PDF_DIR.joinpath(filename), TXT_DIR.joinpath(filename_txt))


if __name__ == "__main__":
    main()
