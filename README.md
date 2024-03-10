# cis6930sp24 -- Assignment1 

Name: Sree Vaishnavi Madireddy

UFID: 87626790

# Assignment Description 
Thid project is designed to censor personal information in text files. It leverages spaCy for entity extraction and provides options to censor names, dates, phone numbers, and addresses. The program recursively processes all text files matching a specified glob pattern, replaces sensitive information with asterisks, and outputs the censored content to new files.

# How to install
pipenv install

## How to run
python text_censor.py --input "*.txt" --output output_directory --names --dates --phones --address --stats stdout

Arguments:

    --input: Glob pattern for input text files.
    --output: Directory to store censored output files.
    --names, --dates, --phones, --address: Flags to specify which entities to censor.
    --stats: Print censoring statistics to "stdout" or "stderr" or any file name
It can be run as follows:
![](https://github.com/VaishnaviReddy99/cis6930sp24-assignment0/blob/test/output.gif)



## Functions
#### main.py \
    extract_entities(text): Uses spaCy to extract entities (names and addresses) from the provided text.

    mask_phone_numbers(text): Masks phone numbers in the given text using a regular expression pattern.

    censor_text(filename, text): Censors specific entities within the text, counts the number of censored words, and returns the censored text.

    readAllFiles(): Recursively traverses all files in the specified input directory, applies censor_text to text files, and writes the censored content to new files in the output directory.

    outputStats(location): Prints or writes to a file the statistics regarding the censoring process.

    parse_args(): Parses command-line arguments using the argparse library.


## Assumptions

## Bugs
