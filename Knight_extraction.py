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
19 dec: 90 min

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
import re

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


def load_and_split_txt(filepath: Path, page_limit: list = None):
    pages = {}
    page_content = ""
    page_number = 2
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if "\x0c" in line:  # Symbol used for page ending
                pages[page_number] = page_content
                page_content = line.split("\x0c")[1]
                page_number += 1
            else:
                page_content += line
    if page_limit == None:
        return pages
    else:
        for key in list(pages.keys()):
            if (key < page_limit[0]) or (key > page_limit[1]):
                del pages[key]
        return pages


def reorder_sentences(pages: dict):
    """ The order of the sentences/lines are not given correct, and thus some logic is applied to fix it 
        1) Sentence can start with "xx. " where x is a digit. 
            Count number of occurences.
        2) Sentence can start with "— "
        3) Sentence ends with ".\n"
        Some words stand alone, and should be connected to the next sentence.
        If sentences are close (i.e. not seperated by \n\n), then they should have priority.

        # Dynamic array of every sentence. 
        # Sentence should have state (Start, End)
        # Sentence should have indication of 

    """
    for page_number, page in pages.items():
        lines = page.split("\n")
        ordered_page = ""
        list_of_sentences = []  # [Sentence, start type, complete sentence?]
        start = True
        for line in lines:
            if line == "":
                continue  # Skip empty lines
            line = line.replace("\xad", "")  # Replace unnesserary characters
            line_start, line_period = sentence_type(line=line)
            if start and (line_start != "other"):
                start = False
            elif start and (line_start == "other"):
                ordered_page += line + "\n"

            if line_start == "num3":
                list_of_sentences.append([line, line_start, line_period])
            elif line_start == "num2":
                # Add to first non complete sentence that starts with one number
                for sen in list_of_sentences:
                    if sen[2] == False and sen[1] == "num1":
                        sen[0] += line
                        sen[1] = "num3"
                        sen[2] = line_period
                        break
                else:
                    list_of_sentences.append([line, line_start, line_period])
            elif line_start == "num1":
                list_of_sentences.append([line, line_start, False])
            elif line_start == "hyphen":
                # TODO: Add numbers for previous date
                list_of_sentences.append([line, line_start, line_period])
            elif start == False and line_start == "other":
                for sen in list_of_sentences:
                    if sen[2] == False and (sen[1] == "num3" or sen[1] == "hyphen"):
                        sen[0] += line
                        sen[2] = line_period
                        break
                else:
                    list_of_sentences.append([line, line_start, line_period])

            # print(ordered_page)

            # print([line, line_start, line_period])
            # if linenum > 10:
            #     break
        for sen in list_of_sentences:
            # print(sen)
            ordered_page += sen[0] + "\n"

        pages[page_number] = ordered_page

    return pages


def sentence_type(line: str):
    """ Detect type of sentence, so one can act on it """
    num1 = bool(re.search("^[\d\s]+[.][^)]", line))  # Starts with a number and period
    num2 = bool(
        re.search("^[\d\s]+[\.][\d\s]+[\.]", line)
    )  # Starts with 2 numbers and period
    num3 = bool(
        re.search("^[\d\s]+[\.][\d\s]+[\.][\d\s]+[\.]", line)
    )  # Starts with 3 numbers and period
    hyphen = bool(re.search("^—\s", line))  # Starts with "— "
    period = bool(re.search("[^\,A-Z][.]$", line)) or bool(
        re.search("[^\,A-Z][.][\s]$", line)
    )  # Ends with and "." and does not contain "," or capital letters right before
    # left_parentheses = len(re.findall("[\(]", line))  # Count ( parentheses
    # right_parentheses = len(re.findall("[\)]", line))  # Count ) parentheses

    end = False
    if num1:
        if num3:
            start = "num3"  # Starts with 3 numbers
        elif num2:
            start = "num2"  # Starts with 2 numbers
        else:
            start = "num1"  # Starts with 1 number
    elif hyphen:
        start = "hyphen"
    else:
        start = "other"
    if period:
        end = True
    return start, end  # , left_parentheses - right_parentheses


def search_pages(pages: dict, searchwords: np.array, header_rows_max: int = 5):
    columns = [
        "Page Title",
        "Header Pages",
        "Pagenumber",
        "Sentence Location %",
        "Word",
        "Sentence",
    ]
    matching_words_info = np.empty(
        (0, len(columns))
    )  # Initialize array of size: rows, columns

    for page_number, page in tqdm(pages.items()):
        sentences = page.split("\n")
        number_of_sentences_on_page = len(sentences)
        title = ""
        header_pages = ""

        for sentence_index, sentence in enumerate(sentences):
            sentence = sentence.lower()
            if sentence_index <= header_rows_max:
                if (("[" in sentence) or ("]" in sentence)) and header_pages == "":
                    header_pages = sentence
                elif title == "":
                    title = sentence

            for word in searchwords:
                if word in sentence:
                    matching_words_info = np.append(
                        matching_words_info,
                        [
                            [
                                title,
                                header_pages,
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
    df_matches = df_matches.astype({columns[2]: "int32"})
    df_matches = df_matches.sort_values(by=[columns[2], columns[3]], ascending=True)
    return df_matches


def write_df_to_excel(filepath: Path, df: pd.DataFrame, sheet_name: str):
    """ Convert the list of results to Excel """
    df.to_excel(filepath, sheet_name=sheet_name, index=False)


def main():
    filepath_cities = DIR.joinpath("Bynavne.xlsx")
    # filepath_cities = DIR.joinpath("sample.xlsx")
    cities = load_seachwords(filepath=filepath_cities)
    filepath_statskalender = DIR.joinpath(
        "Statskalender_txt/Statskalender 1950-pages-100.txt"
        # "test/txt_vars_line_0.6.txt"
    )

    pages = load_and_split_txt(filepath_statskalender)  # , page_limit=[48, 245])
    pages = reorder_sentences(pages=pages)
    # print(pages)

    df_matches = search_pages(pages=pages, searchwords=cities)
    print(df_matches)
    # write_df_to_excel(
    #     filepath=RESULT_DIR.joinpath("1950.xlsx"), df=df_matches, sheet_name="1950"
    # )


if __name__ == "__main__":
    main()

