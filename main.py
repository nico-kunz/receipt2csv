import re
from os import listdir, makedirs, path
import csv
from pypdf import PdfReader
import argparse

PERSON1 = "Name1"
PERSON2 = "Name2"

def debug_print(*args):
    if verbose:
        print(*args)

def find_start(lines):
    """Find the line where the actual receipt data starts"""
    for i, line in enumerate(lines):
        if re.search(r"\d+,\d{2}", line):
            return i
    return -1


def find_end(lines):
    """Find the line where the actual receipt data ends"""
    for i, line in enumerate(lines):
        if re.search(r" *--+", line) or re.search(r" *SUMME", line):
            return i
    return -1


def export_to_csv(file_name, data):
    """Export receipt data to csv file"""
    with open("output/" + file_name, mode="w", encoding="utf-8") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(["Product", "Price", "Together", PERSON1, PERSON2])
        writer.writerows(data)
        writer.writerow(["", "", "", "", "", "Together", "=SUM(C:C)"])
        writer.writerow(["", "", "", "", "", PERSON1, "=SUM(D:D) + SUM(C:C)/2"])
        writer.writerow(["", "", "", "", "", PERSON2, "=SUM(E:E) + SUM(C:C)/2"])

def extract_from_line(line: str):
    """Extract product and price from a line"""
    matches = re.findall(r"-?\d+,\d{2}", line)
    if len(matches) == 0:
        return "", ""
    
    # only use price match at the end of the line
    price = matches[-1]
    product = line.split(price)[0].strip()
    return product, price

def extract_from_file(file):
    """Extract data from a pdf file"""
    # creating a pdf reader object
    reader = PdfReader(file)
    debug_print(len(reader.pages))

    # create page object
    page = reader.pages[0]

    # extract text from page
    text = page.extract_text()

    lines = text.split("\n")

    start_index = find_start(lines)
    end_index = find_end(lines)

    if start_index == -1 or end_index == -1:
        print("Could not find start or end of receipt data for file: " + file)
        return

    split_lines: list[list[str]] = []
    for i in range(start_index, end_index):
        split_lines += list(extract_from_line(lines[i]))

    # remove items that detail amount of product
    for i, line in enumerate(split_lines):
        match = re.match("\d\s+(?:Stk)?\s+x", line[0])
        if match:
            print("MATCH",  split_lines[i][1] + " " + split_lines[i - 1][0])
            split_lines[i - 1][0] = split_lines[i][0].split("x")[0] + "x " + split_lines[i - 1][0]
            removed = split_lines.pop(i)
            debug_print(removed)

    # remove lines that contain "PFAND"
    pfand_keywords = ["PFAND", "LEERGUT"]
    lines_without_pfand = [line for line in split_lines if not any(keyword in line[0] for keyword in pfand_keywords)]

    debug_print(lines_without_pfand)
    export_to_csv(
        str.split(str.split(file, "/")[-1], ".")[0] + ".csv", lines_without_pfand
    )


def main():
    """Main function, extracts data from all files in the pdfs/ folder"""

    argparser = argparse.ArgumentParser(
        description="Extract receipt data from pdf files"
    )
    argparser.add_argument(
        "-f", "--file", help="Extract data from a file or folder", required=True
    )

    argparser.add_argument("-p", "--persons", help="Names of the persons", nargs=2)

    argparser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true", default=False)

    args = argparser.parse_args()

    global PERSON1, PERSON2

    if args.persons:
        PERSON1, PERSON2 = args.persons

    
    global verbose
    verbose = args.verbose

    if path.isdir(args.file):
        files = [ path.join(args.file, f) for f in listdir(args.file) if f.endswith(".pdf") ]
    else:
        files = [args.file]

    # create output dir if not exists
    makedirs("output", exist_ok=True)

    for file in files:
        extract_from_file(file)


if __name__ == "__main__":
    main()
