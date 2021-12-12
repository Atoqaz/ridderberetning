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


def load_seachwords(filepath: str, lowercase: bool = True):
    """ Load excel file with citynames. Extract each unique city from the list. """
    df_cities = pd.read_excel(filepath, names=["Cities"], header=None)
    if lowercase:
        df_cities["Cities"] = df_cities["Cities"].str.lower()
    df_cities = df_cities.drop_duplicates(subset=["Cities"])
    cities = df_cities.to_numpy().T[0]  # Convert to numpy array and transpose
    return cities


def convert_pdf_to_txt(filepath: Path, maxpages: int = 0):
    """ Read pdf, convert it to searchable text & add pagenumber to raw text. """
    rsrcmgr = PDFResourceManager()
    output_string = StringIO()
    device = TextConverter(rsrcmgr, output_string, codec="utf-8", laparams=LAParams())
    with open(filepath, "rb") as pdf_file:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pagenos = set()

        for pagenumber, page in enumerate(
            PDFPage.get_pages(
                pdf_file,
                pagenos,
                maxpages=maxpages,
                password="",
                caching=True,
                check_extractable=True,
            )
        ):
            output_string.write(f"<PDF PAGE SPLIT><Page>{pagenumber}>\n")
            interpreter.process_page(page)
        text = output_string.getvalue()
        device.close()
        output_string.close()
    return text


def search_pdf(pdf_text: str, searchwords: list):
    """ Search pages for the searchwords, and store page number if exist """
    pages = pdf_text.split("<PDF PAGE SPLIT>")[1:]
    location = np.empty((0, 2), str)
    for page in pages:
        for word in searchwords:
            if word in page.lower():
                pagenum = page.split("<Page>")[1].split(">")[0]
                location = np.append(location, [[pagenum, word]], axis=0)
    df_location = pd.DataFrame(location, columns=["Pagenumber", "MatchingWord"])
    return df_location


def main():
    # filepath_cities = DIR.joinpath("Bynavne.xlsx")
    filepath_cities = DIR.joinpath("sample.xlsx")
    filepath_statskalender = DIR.joinpath("Statskalender/sample.pdf")
    # filepath_statskalender = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
    # filepath_statskalender = DIR.joinpath("Statskalender/Statskalender 1950.pdf")
    cities = load_seachwords(filepath=filepath_cities)
    pdf_text = convert_pdf_to_txt(filepath=filepath_statskalender, maxpages=3)
    location = search_pdf(pdf_text=pdf_text, searchwords=cities)
    print(location)


if __name__ == "__main__":
    main()
    pass

