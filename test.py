from time import time, perf_counter
from timeit import timeit

# start = time()

import numpy as np
from pathlib import Path

DIR = Path(__file__).parent

import re


def test_file():
    # filename = DIR.joinpath("Statskalender/Statskalender 1950-pages-100.pdf")
    # filename = DIR.joinpath("test/txt_vars_line_0.6.txt")
    filename = DIR.joinpath("test/txt_vars_line_0.6.txt")
    with open(filename, "r", encoding="utf-8") as file:
        count = 0
        for line in file:
            # result = bool(
            #     re.search("^[\d\s]+[.][^)]", line)
            # )  # xxx # exception if "1.),"" Total 43 correct
            # result = len(re.findall("[\d\s]+[.][^)]", line))
            result = bool(re.search("^—\s", line))  # Line
            # result = bool(re.search("[.][\\n]$", line))  # dot
            # result2 = re.findall(
            #     "^[\d\s]+[\.][\d\s]+[\.][\d\s]+", line
            # )  # xxx all 3 nums
            if result:
                count += 1
                print(line.replace("\n", ""))
                # print(result)

    print(f"Total hits: {count}")


def test_sentences():
    # sentences = [
    #     "29.  1. 29. Hansen, Hans Frederik Valdemar, (D.M.11/i239),Skibsinspektør* under Grønlands Styrelse.",
    #     "30. ",
    #     # "— Bunding, Elias, (Fi.H.R.31.), (N.St.O.31.), ",
    #     # "(S.V.31), Direktør, Kbhvn.",
    #     # "Hjørring.",
    #     # " 25.\n — ",
    #     # "Troéls-Smith, Paul Martin, (H.T.H.), (S.",
    #     # "Kr.3.), Kaptajn*.\n",
    #     # "Godsejer, Eskær.",
    #     "31.), (Po.P.R.4.), (Po.r.K.2.), (S.N.3.), Ge­",
    #     "201  6.10.28. Bl",
    #     "6.10.28. Bl",
    #     "7.  9.28. Olesen, Niels, CDMWnM), (N.St.0.23),.",
    # ]
    sentences = [
        "29.  1. 29. Ha",
        "30. ",
        "31.), (Po.P.R.4.), (Po.r.K.2.), (S.N.3.), Ge­",
        "201  6.10.28. Bl",
        "6.10.28. Bl",
        "7.  9.28. Olesen, (N.St.0.23),.",
        "6. 10.28. Bl",
        "6.10. 28. Bl",
        "6.10.28.Bl",
        "6.10.Bl",
        "11/i239),Skibsinspektør* under Grønlands ",
        "30. ",
        "1. 29. Holdt",
        "9.11. 28. Reimer",
        "Troéls-Smith, Paul Martin, (H.T.H.), (S.",
        "3),. ",
        "Oberstløjtnant*, Landsretssagf., Kbhvn.",
    ]

    for line in sentences:
        # result = re.search("^[\d\s]+[.][^)]", line)  # xxx 1 num
        # result = re.findall("^[\d\s]+[\.][\d\s]+[\.]", line)  # xxx 2 nums
        # result = re.search("^[\d\s]+[\.][\d\s]+[\.][\d\s]+[\.]", line)  # xxx all 3 nums

        # result = re.search("^(â€”)[\s]", line)  # Line (Hyphen)
        # result = re.search("[\.][\\n]$", line)  # dot
        # result = re.search("[^\,][\.]$", line)  # dot
        result = bool(re.search("[^\,][.]$", line)) or bool(
            re.search("[^\,][.][\s]$", line)
        )
        # result = len(re.findall("[\(]", line))  # count parenthases
        # result = len(re.findall("[\)]", line))  # count parenthases
        print(result)


def test():
    # import regex

    # bigString = "AGAHKGHKHASNHADKRGHFKXXX_I_AM_THERE_XXXXXMHHGRFSAHGSKHASGKHGKHSKGHAK"
    # res = regex.findall("(?:I_AM_HERE){e<=1}", bigString)
    # bigString = "AGAHKGHKHASNHADKRGHFKXXX_honekong_XXXXXMHHGRFSAHGSKHASGKHGKHSKGHAK"
    # string = "honsedskong"
    # res = regex.search(f"(?:{string}){{e<=1}}", bigString)
    # print(res)

    start = time()
    # for x in range(1_000_000):
    A = "abcdefghijklmnopqrstuvwxyzæøå"
    A = "abcde"
    index = len(A)
    # x = # A[: max(0, index - 1)] + "X" + A[index:]
    for index, letter in enumerate(A):
        print(f"index: {index}")
        print(f"letter: {letter}")
        print(f"{index}: {A[:index]}")
        # print(f"{index}: {A[: max(0, index - 1)]} - {max(0, index - 1)}")
        print("Result:", A[: index] + "X" + A[index + 1 :])
        print("")
    print(x)
    end = time()
    print(end - start)


if __name__ == "__main__":
    # test_file()
    # test_sentences()
    test()
