# cis6930sp24 -- Assignment1 

Name: Sree Vaishnavi Madireddy

UFID: 87626790

# Assignment Description 
This project is designed to censor personal information in text files. It leverages spaCy for entity extraction and provides options to censor names, dates, phone numbers, and addresses. The program recursively processes all text files matching a specified glob pattern, replaces sensitive information with asterisks, and outputs the censored content to new files.

# How to install
pipenv install

## How to run
Here is a sample command to run:

**pipenv run python censoror.py** --input "*.txt" --output output_directory --names --dates --phones --address --stats stdout

Arguments:

    --input: Glob pattern for input text files.
    --output: Directory to store censored output files.
    --names, --dates, --phones, --address: Flags to specify which entities to censor.
    --stats: Print censoring statistics to "stdout" or "stderr" or any file name
It can be run as follows:
![](https://github.com/VaishnaviReddy99/cis6930sp24-assignment0/blob/test/output.gif)



## Functions
#### censoror.py \
    
    preprocess_text(text): This function removes punctuation characters from the provided text.
    
    extract_entities(text): This function uses spaCy's NER model to identify and extract named entities (persons and addresses) from the preprocessed text. It utilizes a matcher with predefined patterns for names and addresses. Stop words are excluded during entity recognition.

    mask_phone_numbers(text): This function replaces phone numbers in various formats with a sequence of unicode characters (unicode_char * 11). It uses two regular expressions, one for a wider range of formats and another for the specific format "XXX XXX XXXX".
    
    replace_dates(text): This function replaces dates in the text with a sequence of unicode characters (unicode_char * len(date)) corresponding to the length of the date string. It relies on spaCy's NER for date detection (ensure your model is trained for the expected date format).
    
    censor_text(filename, text): This function performs the core text processing. It preprocesses the text, extracts entities, and replaces them with unicode characters. Phone numbers and dates are masked using their respective functions. Statistics on the number of censored words per file are collected.
    
    checkForStopWord(word): This function checks if a word is a stop word (common word) or belongs to a list of additional words to exclude from censoring (e.g., "X", "Graduate", "Date"). Stop words are downloaded from NLTK.
    
    readAllFiles(): This function iterates through all files matching the input_pattern (recursively through subfolders). It reads the content, applies text censoring using censor_text, and writes the transformed content to a new file named "filename.censored" within the output directory.
    
    outputStats(location): This function writes the collected statistics on the number of censored words per file to the specified location. It allows outputting to standard output (stdout), standard error (stderr), or a file.


## Assumptions

    The script operates on the current working directory (os.getcwd()) by default.
    Text files to be processed follow the glob pattern specified by input_pattern (default: "*.txt"). This can be modified using the --input argument.
    The script utilizes the spaCy library for named entity recognition (NER) and regular expressions for phone number and date matching.
    A specific pattern of names and addresses are only utilized

## Bugs
    The script currently has limitations in its information extraction capabilities:

    Limited Date Recognition: The spaCy NER model used might not recognize all date formats.


