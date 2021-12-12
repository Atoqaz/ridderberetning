from pathlib import Path
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_text, extract_pages


DIR = Path(__file__).parent

# filename = DIR.joinpath("Statskalender/Statskalender 1950.pdf")
filename = DIR.joinpath("Statskalender/Matlab Cheatsheet.pdf")
filename = DIR.joinpath("Statskalender/sample.pdf")


# Extract iterable of LTPage objects.
# pages = extract_pages(filename)
# print(pages)


# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfparser import PDFParser
# import io
# import os

# fp = open(filename, "rb")
# rsrcmgr = PDFResourceManager()
# retstr = io.StringIO()
# print(type(retstr))
# codec = "utf-8"
# laparams = LAParams()
# device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
# interpreter = PDFPageInterpreter(rsrcmgr, device)

# page_no = 0
# for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
#     if pageNumber == page_no:
#         interpreter.process_page(page)

#         print(interpreter)

#         # data = retstr.getvalue()

#         # # with open(
#         # #     os.path.join(
#         # #         "Files/Company_list/0010/text_parsed/2017AR", f"pdf page {page_no}.txt"
#         # #     ),
#         # #     "wb",
#         # # ) as file:
#         # #     file.write(data.encode("utf-8"))
#         # data = ""
#         # retstr.truncate(0)
#         # retstr.seek(0)

#     page_no += 1




from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    output_string = StringIO()
    device = TextConverter(rsrcmgr, output_string, codec="utf-8", laparams=LAParams())
    with open(path, "rb") as pdf_file:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        maxpages = 0
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
            interpreter.process_page(page)
            output_string.write(f"<PDF PAGE SPLIT><{pagenumber}>\n")
        text = output_string.getvalue()
        print(text)

        device.close()
        output_string.close()
    return text


convert_pdf_to_txt(filename)
