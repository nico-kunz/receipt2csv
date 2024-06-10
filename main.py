import re
from pypdf import PdfReader


def find_start(lines):
    '''Find the line where the actual receipt data starts'''
    for i, line in enumerate(lines):
        if re.match(r" *EUR$", line):
            return i
    return -1

def find_end(lines):
    '''Find the line where the actual receipt data ends'''
    for i, line in enumerate(lines):
        if re.match(r" *-+", line):
            return i
    return -1


def main():
    '''Main function to extract data from a pdf file'''
    # creating a pdf reader object
    reader = PdfReader('pdfs/REWE-eBon.pdf')

    # printing number of pages in pdf file
    print(len(reader.pages))

    # creating a page object
    page = reader.pages[0]

    # extracting text from page
    #print(page.extract_text())
    text = page.extract_text()

    lines = text.split("\n")
    #print(text.split("\n"))

    start_index = find_start(lines)
    end_index = find_end(lines)

    for j in range(start_index+1, end_index):
        print(re.split(r"  +", lines[j]))

if __name__ == "__main__":
    main()
