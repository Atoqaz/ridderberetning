"""
For each file in the pdf folder, convert it to txt if it has not been done already.
This makes the file faster to seach through.
"""

import os
import re
from tqdm import tqdm
from pathlib import Path


DIR = Path(__file__).parent
PDF_DIR = DIR.joinpath("Statskalender")
TXT_DIR = DIR.joinpath("Statskalender_txt")

import fitz

STR_REMOVE = [
    "\xad",
]


def replace_word_chars(word: str, str_remove: list):
    for string in str_remove:
        word = word.replace(string, "")
    return word


def process_page(page: tuple, offset_x: float, offset_y: float):
    page_text = ""
    x_old, y_old = 0, 0
    word_old = ""
    # (x0, y0, x1, y1, "word", block_no, line_no, word_no)
    # https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractWORDS
    for word in page.get_text("words"):
        x, y = word[0], word[1]  # Get coordinates

        if (
            y > y_old + offset_y
            and (not word[4][0].islower())
            and (not any(x in word[4] for x in [",", "("]))
        ):
            page_text += "\n"
            # pass
        elif abs(x_old - x) <= offset_x:
            page_text += " "

        page_text += replace_word_chars(word=word[4], str_remove=STR_REMOVE)

        x_old, y_old = x, y  # Store old coordinates
    return page_text


def reorder_sentence(page_text: str):
    """Make sentences stay on one line. Sentence starts with date or dash (—). Otherwise append

    Args:
        page_text (str): Text for the page

    Returns:
        str: reorderet sentences
    """
    sentences = page_text.split("\n")
    page_text_new = ""
    first_sentence = True
    for sentence in sentences:
        if sentence == "":
            pass
        elif first_sentence:
            page_text_new += sentence
            first_sentence = False
        elif sentence[0] == "\x0c":
            page_text_new += sentence
        elif re.match(
            r"([\d]+[.][\s]*){2,3}|(— )|(\d\d\d\d[.]? [.]?[\d]{1,2}[\s.])", sentence
        ):
            page_text_new += "\n" + sentence.rstrip("\n")
        else:
            page_text_new += sentence
    return page_text_new


def extract_text_from_pdf(filepath_pdf):
    text = ""
    with fitz.open(filepath_pdf) as pdf:
        for page_num in tqdm(range(len(pdf))):
            text += f"\n\x0c{page_num+1}\x0c\n"  # pagenumber in separate line
            if page_num + 1 == 132:
                print("page")
            page = pdf[page_num]
            page_text = process_page(page=page, offset_x=100, offset_y=5)
            page_text = reorder_sentence(page_text)
            text += page_text
    return text


def pdf_to_txt(filepath_pdf: Path, filepath_txt: Path, layout_settings: dict):
    print(filepath_pdf)
    text = extract_text_from_pdf(filepath_pdf)
    with open(filepath_txt, "w+", encoding="utf-8") as txt_file:
        for line in text:
            txt_file.write(line)


def convert_pdf_folder_to_txt():
    pdf_files = os.listdir(PDF_DIR)
    txt_files = os.listdir(TXT_DIR)
    for filename in tqdm(pdf_files):
        print(filename)
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
