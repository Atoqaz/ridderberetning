"""
Purpose with the file is to generate a list of people from greenland from a list of PDF's who has recieved a medal.
The list should contain the following, that matches a city name:
- PDF line number
- The line string
- Possible date
"""

"""
Samlet arbejdstid:
12 dec: 60 min

"""


import numpy as np
import pandas as pd
from pathlib import Path
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

DIR = Path(__file__).parent


def load_seachwords(filepath: str):
    """ Load excel file with citynames. Extract each unique city from the list. """
    df_cities = pd.read_excel(filepath, names=["Cities"])
    df_cities = df_cities.drop_duplicates(subset=["Cities"])
    cities = df_cities.to_numpy().T[0]  # Convert to numpy array and transpose
    return cities


def convert_pdf_to_txt(filepath, maxpages=0):
    rsrcmgr = PDFResourceManager()
    output_string = StringIO()
    device = TextConverter(rsrcmgr, output_string, codec="utf-8", laparams=LAParams())
    with open(filepath, "rb") as pdf_file:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # maxpages = 0
        caching = True
        pagenos = set()

        for pagenumber, page in enumerate(
            PDFPage.get_pages(
                pdf_file,
                pagenos,
                maxpages=maxpages,
                password="",
                caching=caching,
                check_extractable=True,
            )
        ):
            output_string.write(f"<PDF PAGE SPLIT><Page {pagenumber}>\n")
            interpreter.process_page(page)
        text = output_string.getvalue()
        device.close()
        output_string.close()
    return text


def search_pdf(pdf_text, searchwords):
    pages = pdf_text.split("<PDF PAGE SPLIT>")
    # for each page, for each word. If word matches write page number and line to excel doc
    print(pages)


def main():
    filepath_cities = DIR.joinpath("Bynavne.xlsx")
    filepath_statskalender = DIR.joinpath("Statskalender/sample.pdf")
    filepath_statskalender = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
    # filepath_statskalender = DIR.joinpath("Statskalender/Statskalender 1950.pdf")
    cities = load_seachwords(filepath=filepath_cities)
    pdf_text = convert_pdf_to_txt(filepath=filepath_statskalender, maxpages=3)
    search_pdf(pdf_text=pdf_text, searchwords=cities)
    # print(pdf_text)


if __name__ == "__main__":
    main()
    pass

