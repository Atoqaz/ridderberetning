"""
Purpose with the file is to generate a list of people from greenland from a list of PDF's who has recieved a medal.
The list should contain the following, that matches a city name:
- PDF line number (Done)
- The line string (Done)
- Possible date (Maybe)
- Only reorder pages with matches
"""

"""
Samlet arbejdstid:
12 dec: 200 min
16 dec: 70 min
18 dec: 120 min
19 dec: 90 min
27 dec: 240 min
30 dec: 60 min
09 jan: 120 min

Total: 15 h 0 min

Improvements:


Thinks to mind:
    - Abbreviations (København -> Kbhvn)
    - Incorrect reading of words (Hongkong -> Honekong)

    - Multicore speed up (maybe)
    - Line split " | " is good
    - Search include period?
    - Add removal of special characters: Like Ú -> U and Î -> I
"""


import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import re
import regex
import os

DIR = Path(__file__).parent
RESULT_DIR = DIR.joinpath("Statskalender_results")
TXT_DIR = DIR.joinpath("Statskalender_txt")
OUTPUT_FILE = DIR.joinpath("Result.xlsx")
EXACT_MATCH = True  # Match is not case sensitive


def load_seachwords(filepath: Path):
    """ Load excel file with citynames. Extract each unique city from the list. """
    df_cities = pd.read_excel(filepath, names=["Cities"], header=None)  # Read file
    df_cities = df_cities.drop_duplicates(subset=["Cities"])  # Remove duplicate
    cities = df_cities.to_numpy().T[0]  # Convert to numpy array and transpose
    # Remove last space in word
    for word_index, word in enumerate(cities):
        if word[-1] == " ":
            cities[word_index] = word[:-1]
    return cities


def generate_pertubations(words: np.array):
    """ Create 1 letter pertubations for each word, for every letter in the word. 
        Generate word without special characters """

    new_words = []
    alphabet = "abcdefghijklmnopqrstuvwxyzæøå"
    count = 0
    word_pertubation = ""
    for word in words:
        for letter_index, letter in enumerate(word):
            capital = letter.isupper()
            for char in alphabet:
                if capital:
                    char = char.upper()
                word_pertubation = word[:letter_index] + char + word[letter_index + 1 :]
                new_words.append(word_pertubation)
                count += 1

    words = np.append(words, new_words)
    return np.unique(words)


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

        for sen in list_of_sentences:
            ordered_page += sen[0] + "\n"

        pages[page_number] = ordered_page

    return pages


def reorder_sentences_on_page(page: str):
    """ The order of the sentences/lines are not given correct, and thus some logic is applied to fix it 
        1) Sentence can start with "xx. " where x is a digit. 
            Count number of occurences.
        2) Sentence can start with "— "
        3) Sentence ends with ".\n"
        Some words stand alone, and should be connected to the next sentence.
        If sentences are close (i.e. not seperated by \n\n), then they should have priority.

    """
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

    for sen in list_of_sentences:
        ordered_page += sen[0] + "\n"
    return ordered_page


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


def search_pages(
    pages: dict, searchwords: np.array, header_rows_max: int = 5, exact_match=False
):
    """ For each page, if a keyword matches a sentence add both to the dataframe """
    columns = [
        "Page Title",
        "Header Pages",
        "Pagenumber",
        "Sentence Quarter",
        "Word",
        "Sentence",
    ]
    matching_words_info = np.empty(
        (0, len(columns))
    )  # Initialize array of size: rows, columns

    for page_number, page in tqdm(pages.items()):
        # If any word in the page, reorder page
        page_reordered = False
        temp_page = page.replace("-\n ", "").replace("-\n", "").replace("\n", "")
        for word in searchwords:
            if not exact_match:
                word_in_sentence = bool(regex.search(f"(?:{word}){{e<=1}}", page))
            if (exact_match and (word in temp_page)) or (
                not exact_match and word_in_sentence
            ):

                page = reorder_sentences_on_page(page=page)
                page_reordered = True
                break

        if page_reordered:
            title = ""
            header_pages = ""
            sentences = page.split("\n")
            number_of_sentences_on_page = len(sentences)

            for sentence_index, sentence in enumerate(sentences):
                if sentence_index <= header_rows_max:
                    if (
                        ("[" in sentence)
                        or ("]" in sentence)
                        or (re.search("[0-9]", sentence))
                    ) and header_pages == "":  # or only numeric
                        header_pages = sentence
                    elif title == "":
                        title = sentence

                for word in searchwords:
                    if not exact_match:
                        word_in_sentence = bool(
                            regex.search(f"(?:{word}){{e<=1}}", sentence)
                        )
                    if (exact_match and word in sentence) or (
                        not exact_match and word_in_sentence
                    ):
                        sentence_location = round(
                            sentence_index / number_of_sentences_on_page * 100
                        )
                        if sentence_location <= 25:
                            location = 1
                        elif sentence_location <= 50:
                            location = 2
                        elif sentence_location <= 75:
                            location = 3
                        else:
                            location = 4
                        matching_words_info = np.append(
                            matching_words_info,
                            [
                                [
                                    title,
                                    header_pages,
                                    page_number,
                                    location,
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
    txt_files = [x for x in os.listdir(TXT_DIR) if ".txt" in x]
    for file_index, filename in enumerate(txt_files, 1):
        if ".txt" in filename:
            print(f"[{file_index}] {filename}")

    print(f"\nSearch method: Exact Match = {EXACT_MATCH}\n")

    # Select file
    while True:
        try:
            selected_file_index = input("Select file: ")
            selected_file = txt_files[int(selected_file_index) - 1]
            filepath = TXT_DIR.joinpath(selected_file)
            print(f"File selected: {selected_file}")
            break
        except IndexError:
            print("\nNumber not in list. Please try again.\nPress ctrl + C to exit.\n")

    # Select page numbers
    pagenumber_min = int(input("Select starting pdf pagenumber: "))
    pagenumber_max = int(input("Select ending pdf pagenumber: "))
    page_limit = [pagenumber_min, pagenumber_max]

    sheet_name = selected_file[-8:-4]
    main_file_search(filepath=filepath, page_limit=page_limit, sheet_name=sheet_name)


def main_file_search(filepath: Path, page_limit: list, sheet_name: str):
    filepath_cities = DIR.joinpath("Bynavne.xlsx")
    cities = load_seachwords(filepath=filepath_cities)
    cities = generate_pertubations(words=cities)
    pages = load_and_split_txt(filepath=filepath, page_limit=page_limit)
    # pages = reorder_sentences(pages=pages)
    df_matches = search_pages(pages=pages, searchwords=cities, exact_match=EXACT_MATCH)
    write_df_to_excel(
        filepath=RESULT_DIR.joinpath(f"{sheet_name}.xlsx"),
        df=df_matches,
        sheet_name=sheet_name,
    )


def test():
    filepath_cities = DIR.joinpath("Bynavne.xlsx")
    cities = load_seachwords(filepath=filepath_cities)
    cities = generate_pertubations(words=cities)


if __name__ == "__main__":
    main()
    # test()

