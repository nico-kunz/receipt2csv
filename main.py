import re
import csv
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


def export_to_csv(data):
    '''Export receipt data to csv file'''
    with open('receipt.csv', mode='w', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Product", "Price"])
        writer.writerows(data)
        writer.writerow(["", "", "Together", "=SUM(B:B)"])


def main():
    '''Main function to extract data from a pdf file'''
    # creating a pdf reader object
    reader = PdfReader('pdfs/REWE-eBon.pdf')

    # printing number of pages in pdf file
    print(len(reader.pages))

    # creating a page object
    page = reader.pages[0]

    # extracting text from page
    text = page.extract_text()

    lines = text.split("\n")

    start_index = find_start(lines)
    end_index = find_end(lines)

    split_lines = []
    for j in range(start_index+1, end_index):
        split_lines += [re.split(r"  +", lines[j])]

    # remove lines that contain "PFAND"
    lines_without_pfand = list(
        filter(lambda x: "PFAND" not in x[0], split_lines))

    # remove items that detail amount of product
    for (i, line) in enumerate(lines_without_pfand):

        if line[0] == '':
            lines_without_pfand[i-1][0] = lines_without_pfand[i][1] + \
                " " + lines_without_pfand[i-1][0]
            lines_without_pfand.pop(i)

    # filter out letters at the end of price
    for (i, line) in enumerate(lines_without_pfand):
        if re.match(r"\d+,\d{2}", line[1]):
            lines_without_pfand[i][1] = re.sub(r"[a-zA-Z]|\s", "", line[1])

    print(lines_without_pfand)
    export_to_csv(lines_without_pfand)


if __name__ == "__main__":
    main()
