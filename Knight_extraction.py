"""
Purpose with the file is to generate a list of people from greenland from a list of PDF's who has recieved a medal.
The list should contain the following, that matches a city name:
- PDF line number (Done)
- The line string
- Possible date
"""

"""
Samlet arbejdstid:
12 dec: 150 min

Improvements:
    - Convert pdf to txt and store it for further searches.
    -> Check if txt exist, and use it instead of pdf.

Thinks to mind:
    - Abbreviations (København -> Kbhvn)
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
OUTPUT_FILE = DIR.joinpath("Result.xlsx")
Calender = "1950"


def load_seachwords(filepath: str):
    """ Load excel file with citynames. Extract each unique city from the list. """
    df_cities = pd.read_excel(filepath, names=["Cities"], header=None)  # Read
    df_cities["Cities"] = df_cities["Cities"].str.lower()  # Convert to lowercase
    df_cities = df_cities.drop_duplicates(subset=["Cities"])  # Remove duplicate
    cities = df_cities.to_numpy().T[0]  # Convert to numpy array and transpose
    return cities


def convert_pdf_to_txt(filepath: Path, maxpages: int = 0):
    """ Read pdf, convert it to searchable text & add pagenumber. """
    resource_manager = PDFResourceManager()
    output_string = StringIO()
    converter = TextConverter(
        resource_manager, output_string, codec="utf-8", laparams=LAParams()
    )
    with open(filepath, "rb") as pdf_file:
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
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
            output_string.write(f"^PDF PAGE SPLIT^^page^{pagenumber}^\n")
            page_interpreter.process_page(page)

        text = output_string.getvalue()

        converter.close()
        output_string.close()
    return text


def extract_text_from_pdf(filepath: Path, maxpages: int = 0):
    """
    Helper function to extract the plain text from .pdf files

    :param filepath: path to PDF file to be extracted
    :return: iterator of string of extracted text
    """
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    with open(filepath, "rb") as pdf_file:
        for page in PDFPage.get_pages(pdf_file, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            output_string = StringIO()
            converter = TextConverter(
                resource_manager, output_string, codec="utf-8", laparams=LAParams()
            )
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            page_text = output_string.getvalue()
            yield page_text

            # close open handles
            converter.close()
            output_string.close()


def search_pdf(filepath: str, searchwords: list):
    """ Search pages for the searchwords, and store page number if exist """
    # pages = pdf_text.split("^PDF PAGE SPLIT^")[
    #     1:
    # ]  # Split text into pages, ignoring first empty page
    columns = ["Pagenumber", "SentenceNumber", "SentencesInPage", "Word", "Sentence"]
    location = np.empty((0, len(columns)))  # Initialize array of size: rows, columns

    pages = extract_text_from_pdf(filepath=filepath)

    for pagenum, page in enumerate(pages):
        page = page.lower()
        # pagenum = page.split("^page^")[1].split("^")[0]
        # pagenum = -1
        sentences = None
        # print(page)
        for word in searchwords:
            if word in page:

                if sentences == None:
                    sentences = page.split("\n\n")  # TODO: Improve split
                    len_lentences = len(sentences)

                for sentence_idx, sentence in enumerate(sentences):
                    if (sentence != "\n") and (word in sentence):
                        # print(sentence)
                        location = np.append(
                            location,
                            [[pagenum, sentence_idx, len_lentences, word, sentence]],
                            axis=0,
                        )
    df_location = pd.DataFrame(location, columns=columns,)
    df_location = df_location.astype({columns[1]: "int32"})
    df_location = df_location.sort_values(by=columns[1], ascending=True)
    print(df_location)
    return df_location


def write_df_to_excel(filepath: Path, df: pd.DataFrame, sheet_name: str):
    """ Convert the list of results to Excel """
    df.to_excel(filepath, sheet_name=sheet_name)


def main():
    # filepath_cities = DIR.joinpath("Bynavne.xlsx")
    # filepath_cities = DIR.joinpath("sample.xlsx")
    filepath_cities = DIR.joinpath("sample_advanced.xlsx")

    # filepath_statskalender = DIR.joinpath("Statskalender/sample.pdf")
    # filepath_statskalender = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
    filepath_statskalender = DIR.joinpath(
        "Statskalender/Statskalender 1950-pages-100.pdf"
    )

    # filepath_statskalender = DIR.joinpath("Statskalender/Statskalender 1950.pdf")
    cities = load_seachwords(filepath=filepath_cities)
    print("Converting pdf...")
    # pdf_text = convert_pdf_to_txt(filepath=filepath_statskalender, maxpages=0)
    # pdf_text = extract_text_from_pdf(filepath=filepath_statskalender)
    pdf_text = search_pdf(filepath=filepath_statskalender, searchwords=cities)
    print("Seaching pdf...")
    print(pdf_text)
    # df_location = search_pdf(pdf_text=pdf_text, searchwords=cities)
    # write_df_to_excel(
    #     filepath=OUTPUT_FILE, df=df_location, sheet_name=Calender,
    # )
    # print(df_location)


if __name__ == "__main__":
    main()
    pass


# def search_pdf(pdf_text: str, searchwords: list):
#     """ Search pages for the searchwords, and store page number if exist """
#     pages = pdf_text.split("^PDF PAGE SPLIT^")[
#         1:
#     ]  # Split text into pages, ignoring first empty page
#     columns = ["Pagenumber", "SentenceNumber", "SentencesInPage", "Word", "Sentence"]
#     location = np.empty((0, len(columns)))  # Initialize array of size: rows, columns

#     for page in pages:
#         page = page.lower()
#         pagenum = page.split("^page^")[1].split("^")[0]
#         sentences = None
#         # print(page)
#         for word in searchwords:
#             if word in page:

#                 if sentences == None:
#                     sentences = page.split("\n\n")  # TODO: Improve split
#                     len_lentences = len(sentences)

#                 for sentence_idx, sentence in enumerate(sentences):
#                     if (sentence != "\n") and (word in sentence):
#                         # print(sentence)
#                         location = np.append(
#                             location,
#                             [[pagenum, sentence_idx, len_lentences, word, sentence]],
#                             axis=0,
#                         )
#     df_location = pd.DataFrame(location, columns=columns,)
#     df_location = df_location.astype({columns[1]: "int32"})
#     df_location = df_location.sort_values(by=columns[1], ascending=True)
#     print(df_location)
#     return df_location
