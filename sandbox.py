# %%

import re


def set_header(sentence: str, header_pages: str = "", title: str = ""):
    """Extract first and last number:
    Set headerpages to f"[{first} - {last}]"
    Set title to rest
    """
    if (header_pages == "") or (title == ""):
        first_non_digit_pos = None
        last_non_digit_pos = None
        if "[" in sentence:
            first_non_digit_pos = sentence.find("[")
            last_non_digit_pos = sentence.find("]")
            header_pages = sentence[
                first_non_digit_pos + 1 : last_non_digit_pos
            ].replace("—", "-")
            if first_non_digit_pos < 2:
                last_position = -1
                for pos, char in enumerate(sentence[last_non_digit_pos + 1 :]):
                    if char.isdigit():
                        last_position = pos + last_non_digit_pos + 1
                        break
                title = sentence[last_non_digit_pos + 1 : last_position]
            else:
                title = sentence[:first_non_digit_pos]
        else:

            for pos, (char, char_reverse) in enumerate(zip(sentence, sentence[::-1])):
                if (not char.isdigit()) and (first_non_digit_pos is None):
                    first_non_digit_pos = pos
                if (not char_reverse.isdigit()) and (last_non_digit_pos is None):
                    last_non_digit_pos = len(sentence) - pos

            first_num = sentence[:first_non_digit_pos]
            second_num = sentence[last_non_digit_pos:]
            header_pages = f"{first_num}-{second_num}"
            pos = sentence.find(str(second_num))
            title = f"{sentence[first_non_digit_pos: pos]}"

    return header_pages, title


sentences = [
    "[329—331]Riddere af Dannebrogordenen.",
    "Riddere af Dannebrogordenen.[331—335]",
    "20Riddere af Dannebrogordenen.21",
    "[210 a—214 a] Riddere af Dannebrogordenen.26.3.211 4.21.25.211a 2.6.19.27.10.24.29.30.212 K20.25.7.12.212 a 14.20.24.",
]

for sentence in sentences:
    header_pages, title = set_header(sentence)
    print(f"sentence: {sentence}")
    print(f"header_pages: {header_pages}")
    print(f"title: {title}")
    print("")
