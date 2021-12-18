"""
Purpose with the file is to generate a list of people from greenland from a list of PDF's who has recieved a medal.
The list should contain the following, that matches a city name:
- PDF line number (Done)
- The line string
- Possible date
"""

"""
Samlet arbejdstid:
12 dec: 200 min
16 dec: 70 min
18 dec: 120 min

Improvements:
    -> Split pdf in columns, as to not to get interferrence between them.
        - This has to be done dynamically for each page, as separater position varies
    -> Page title (line 1) in output 

Thinks to mind:
    - Abbreviations (København -> Kbhvn)
    - Linesplit (-\n)
"""


import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm

DIR = Path(__file__).parent
RESULT_DIR = DIR.joinpath("Statskalender_results")
OUTPUT_FILE = DIR.joinpath("Result.xlsx")
Calender = "1950"


def load_seachwords(filepath: Path):
    """ Load excel file with citynames. Extract each unique city from the list. """
    df_cities = pd.read_excel(filepath, names=["Cities"], header=None)  # Read
    df_cities["Cities"] = df_cities["Cities"].str.lower()  # Convert to lowercase
    df_cities = df_cities.drop_duplicates(subset=["Cities"])  # Remove duplicate
    cities = df_cities.to_numpy().T[0]  # Convert to numpy array and transpose
    return cities


def load_and_split_txt(filepath: Path):
    pages = {}
    page_content = ""
    page_number = 2
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if "\x0c" in line:  # Symbol used for page ending
                pages[page_number] = page_content
                page_content = ""
                page_number += 1
            else:
                page_content += line
    return pages


def search_pages(pages: dict, searchwords: np.array):
    columns = ["Pagenumber", "Sentence Location %", "Word", "Sentence"]
    matching_words_info = np.empty(
        (0, len(columns))
    )  # Initialize array of size: rows, columns

    for page_number, page in tqdm(pages.items()):
        sentences = page.split("\n\n")
        number_of_sentences_on_page = len(sentences)
        for sentence_index, sentence in enumerate(sentences):
            sentence = sentence.lower()
            for word in searchwords:
                if word in sentence:
                    matching_words_info = np.append(
                        matching_words_info,
                        [
                            [
                                page_number,
                                round(
                                    sentence_index / number_of_sentences_on_page * 100
                                ),
                                word,
                                sentence,
                            ]
                        ],
                        axis=0,
                    )

    df_matches = pd.DataFrame(matching_words_info, columns=columns,)
    df_matches = df_matches.astype({columns[0]: "int32"})
    df_matches = df_matches.sort_values(by=[columns[0], columns[1]], ascending=True)
    return df_matches


def write_df_to_excel(filepath: Path, df: pd.DataFrame, sheet_name: str):
    """ Convert the list of results to Excel """
    df.to_excel(filepath, sheet_name=sheet_name, index=False)


def main():
    filepath_cities = DIR.joinpath("Bynavne.xlsx")
    # filepath_cities = DIR.joinpath("sample.xlsx")
    # filepath_cities = DIR.joinpath("sample_advanced.xlsx")

    cities = load_seachwords(filepath=filepath_cities)
    # filepath_statskalender = DIR.joinpath("Statskalender/sample.pdf")
    # filepath_statskalender = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
    # filepath_statskalender = DIR.joinpath("Statskalender_txt/Statskalender 1950.txt")
    filepath_statskalender = DIR.joinpath(
        "Statskalender_txt/Statskalender 1950-pages-100.txt"
    )

    pages = load_and_split_txt(filepath_statskalender)
    df_matches = search_pages(pages=pages, searchwords=cities)
    write_df_to_excel(
        filepath=RESULT_DIR.joinpath("1950.xlsx"), df=df_matches, sheet_name="1950"
    )


if __name__ == "__main__":
    main()

