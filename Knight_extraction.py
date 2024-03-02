"""
Purpose with the file is to generate a list of people from greenland, based on their city, from a list of PDF's of those who has recieved a medal.
The list should contain the following, that matches a city name:
- PDF line number
- The line string

Thinks to mind:
    - Abbreviations (København -> Kbhvn) are not accounted for.
    - Incorrect reading of letters make it difficult.
    - If word is on 2 seperate lines, it will not be included.
    - If the word is not capitized correct, it will not be included.
"""

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path

DIR = Path(__file__).parent
CITY_DIR = DIR.joinpath("Bynavne.xlsx")
RESULT_DIR = DIR.joinpath("Statskalender_results")
TXT_DIR = DIR.joinpath("Statskalender_txt")
EXACT_MATCH = True  # Obs: Match is not case sensitive
INCLUDE_PERIOD = True
ALPHABET = "abcdefghijklmnopqrstuvwxyzæøå"


def load_seachwords(filepath: Path):
    """Load excel file with citynames. Extract each unique city from the list."""
    df_cities = pd.read_excel(filepath, names=["Cities"], header=None)  # Read file
    df_cities = df_cities.drop_duplicates(subset=["Cities"])  # Remove duplicate
    df_cities = df_cities.dropna()
    cities = df_cities.to_numpy().T[0]  # Convert to numpy array and transpose
    # Remove last space in word
    for word_index, word in enumerate(cities):
        if word[-1] == " ":
            cities[word_index] = word[:-1]
    return cities


def generate_pertubations(words: np.array):
    """Create 1 letter pertubations for each word, for every letter in the word.
    Generate word without special characters"""

    new_words = []
    count = 0
    word_pertubation = ""
    for word in words:
        for letter_index, letter in enumerate(word):
            capital = letter.isupper()
            for char in ALPHABET:
                if capital:
                    char = char.upper()
                word_pertubation = word[:letter_index] + char + word[letter_index + 1 :]
                if INCLUDE_PERIOD:
                    word_pertubation = word_pertubation + "."
                new_words.append(word_pertubation)
                count += 1

    words = np.append(words, new_words)
    return np.unique(words)


def load_and_split_txt(filepath: Path):
    pages = {}
    page_number = 0
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if line == "\n":
                pass
            elif (line[0] == "\x0c") and (
                line[-2:] == "\x0c\n"
            ):  # Symbol used for page number in start of page
                page_number = int(line[1:-2])
                pages[page_number] = ""
            else:
                pages[page_number] += line
    return pages


def limit_pages(pages: dict, page_limit: list = None):
    if page_limit == None:
        return pages
    else:
        for key in list(pages.keys()):
            if (key < page_limit[0]) or (key > page_limit[1]):
                del pages[key]
        return pages


def set_header(sentence: str, header_pages: str, title: str):
    """Extract first and last number:
    Set headerpages to f"[{first} - {last}]"
    Set title to rest
    """
    if (header_pages == "") or (title == ""):
        first_non_digit_pos = None
        last_non_digit_pos = None
        for pos, char in enumerate(sentence):
            if (not char.isdigit()) and (first_non_digit_pos is None):
                first_non_digit_pos = pos
        for pos, char in enumerate(sentence[::-1]):
            if (not char.isdigit()) and (last_non_digit_pos is None):
                last_non_digit_pos = len(sentence) - pos
                break
        if pos <= 3:  # max 3 digits
            header_pages = (
                f"{sentence[:first_non_digit_pos]}-{sentence[last_non_digit_pos:]}"
            )
            title = f"{sentence[first_non_digit_pos: last_non_digit_pos]}"
        else:
            header_pages = sentence[:first_non_digit_pos]
            title = f"{sentence[first_non_digit_pos:]}"
    return header_pages, title


def search_pages(
    pages: dict, searchwords: np.array, header_rows_max: int = 5, exact_match=False
):
    """For each page, if a keyword matches a sentence add both to the dataframe"""
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
        # Screening
        word_in_page = False
        for word in searchwords:
            if word in page:
                word_in_page = True  # Effiency?
                break

        # Detailed extraction
        if word_in_page:
            title = ""
            header_pages = ""
            sentences = page.split("\n")
            number_of_sentences_on_page = len(sentences)
            for sentence_index, sentence in enumerate(sentences):
                header_pages, title = set_header(
                    sentence=sentence, header_pages=header_pages, title=title
                )

                for word in searchwords:
                    if word in sentence:
                        sentence_location = round(
                            sentence_index / number_of_sentences_on_page * 100
                        )
                        location = sentence_location // 25
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
    df_matches = pd.DataFrame(
        matching_words_info,
        columns=columns,
    )
    df_matches = df_matches.astype({columns[2]: "int32"})
    df_matches = df_matches.sort_values(by=[columns[2], columns[3]], ascending=True)
    return df_matches


def write_df_to_excel(filepath: Path, df: pd.DataFrame, sheet_name: str):
    """Convert the list of results to Excel"""
    df.to_excel(filepath, sheet_name=sheet_name, index=False)


def get_user_input(txt_files):
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

    return filepath, page_limit


def list_files():
    txt_files = [x for x in os.listdir(TXT_DIR) if ".txt" in x]
    for file_index, filename in enumerate(txt_files, 1):
        if ".txt" in filename:
            print(f"[{file_index}] {filename}")
    return txt_files


def main():
    txt_files = list_files()
    print(f"\nSearch method: Exact Match = {EXACT_MATCH}\n")
    filepath, page_limit = get_user_input(txt_files)
    # filepath = TXT_DIR.joinpath(txt_files[0]) #TODO: Test
    # page_limit = [44, 169] #TODO: Test
    # sheet_name = "1901" #TODO: Test

    sheet_name = filepath.stem[-4:]  # Year: Assumes last for chars are the year
    main_file_search(filepath=filepath, page_limit=page_limit, sheet_name=sheet_name)


def main_file_search(filepath: Path, page_limit: list, sheet_name: str):
    filepath_cities = CITY_DIR
    cities = load_seachwords(filepath=filepath_cities)
    cities = generate_pertubations(words=cities)
    pages = load_and_split_txt(filepath=filepath)
    if page_limit:
        pages = limit_pages(pages=pages, page_limit=page_limit)
    df_matches = search_pages(pages=pages, searchwords=cities, exact_match=EXACT_MATCH)
    write_df_to_excel(
        filepath=RESULT_DIR.joinpath(f"{sheet_name}.xlsx"),
        df=df_matches,
        sheet_name=sheet_name,
    )


if __name__ == "__main__":
    main()
