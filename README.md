# Receipt2CSV
## How to Use

### Install Dependencies
To use this program, clone the repo and then execute this in the root directory of the project to install the dependencies:
```
pip install -r requirements.txt
```

### Run
Put the pdfs to extract in a folder of your choice and run:
```
python main.py -f <folder_path/pdf_path> 
```

### Command-Line Options
``-f`` or ``--file``: Path to a specific file or folder containing PDF receipts. Required parameter.  
Example: ``python main.py -f pdfs/``

``-p`` or ``--persons``: Specify two person names for splitting costs.  
Example: ``python main.py -f pdfs/ -p "Person1" "Person2"``. Defaults to "Name1" and "Name2".

``-v`` or ``--verbose``: Enable verbose output for debugging purpose
