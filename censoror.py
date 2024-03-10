import sys
import argparse
import os
import spacy
import shutil
import re
import glob
from spacy.matcher import Matcher

# Define the output directory name
output_directory_name = 'output'
unicode_char = '\u2588'
statsOP = []
input_pattern = ".txt"

def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")  # Load spaCy model
    matcher = Matcher(nlp.vocab)
    name_pattern = [
      # Option 1: First Name, Last Name
      [{"POS": "NOUN"} | {"POS": "TITLE"} | {"TEXT": "^[A-Z]\."}, {"POS": "PROPN"}],
      # Option 2: Full Name
      [{"POS": "PROPN"}],  # Capture single words (full names)
    ]
    address_pattern = [
        [{"LIKE_NUM": True}, {"IS_PUNCT": True, "OP": "?"}, {"POS": "NOUN", "OP": "?"}],  # Street number and optional punctuation
        [{"POS": "PROPN", "OP": "+"}],  # City (at least one proper noun)
        [{"POS": "PROPN"} | {"POS": "GPE"}],  # Optional state or geopolitical entity
        [{"POS": "NUM", "LENGTH": 5}]  # Pincode (5 digits)
    ]

    matcher.add("PERSON",name_pattern)
    matcher.add("ADDRESS", address_pattern)

    doc = nlp(text)
    matches = matcher(doc)
    entities = []
    #print(matches)
    for label, start, end,  in matches:
        span = doc[start:end]
        entities.append((label, span.text))
    return entities

def mask_phone_numbers(text):
    # Define a regular expression pattern for matching phone numbers
    local_pattern = re.compile(r'^\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}$')
    # Replace phone numbers with '**'
    masked_text = re.sub(local_pattern, unicode_char*11, text)
    return masked_text

def censor_text(filename, text):
    entities = extract_entities(text)
    entity_set = {entity for label, entity in entities}
    result_str = ""
    count = 0
    for word in text.split(" "):
        if word in entity_set:
            count = count + 1
            result_str = result_str + " " + unicode_char * len(word)
        else:
            result_str = result_str + " " + word
    result_str = mask_phone_numbers(result_str)
    statsOP.append("File : " + filename+" No.of words censored : " + str(count))
    print(filename)
    return result_str


def readAllFiles():
    # Iterate through all folders, subfolders, and files recursively
    print(input_pattern)
    full_pattern = os.path.join(os.getcwd(), '**', input_pattern)
    matching_files = glob.glob(full_pattern, recursive=True)

    print(matching_files)
    for file in matching_files:
        destination_path = os.path.join(output_directory, os.path.basename(file)+"censored")
        # Read the content of the file
        with open(file, 'r', encoding='utf-8') as file_content:
            content = file_content.read()

        # Apply your transformation to the content (e.g., add some text)
        transformed_content = censor_text(file, content)
        # Write the transformed content to the destination file
        with open(destination_path, 'w', encoding='utf-8') as destination_file:
            destination_file.write(transformed_content)


    print(f"All text files recursively transformed and saved to {output_directory}")




def outputStats(location):
    op = "\n".join(statsOP)
    if location == "stdout":
        print(op)
    elif location == "stderr":
        print(op,file=sys.stderr)
    else:
        with open(location, 'w', encoding='utf-8') as destination_file:
            destination_file.write(op)


def parse_args():
  """Parses command-line arguments.

  Returns:
    A namespace object containing parsed arguments.
  """

  parser = argparse.ArgumentParser(description="Censor personal information in text files.")

  # Input arguments
  parser.add_argument("--input", type=str, required=False,
                      help="Glob pattern for input text files (e.g., '*.txt').")

  # Output arguments
  parser.add_argument("--output", type=str, required=False,
                      help="Directory to store censored output files.")

  # Censoring options (flags)
  parser.add_argument("--names", action="store_true", default=False,
                      help="Censor names in the text files.")
  parser.add_argument("--dates", action="store_true", default=False,
                      help="Censor dates in the text files.")
  parser.add_argument("--phones", action="store_true", default=False,
                      help="Censor phone numbers in the text files.")
  parser.add_argument("--address", action="store_true", default=False,
                      help="Censor addresses in the text files.")

  # Output options
  parser.add_argument("--stats", type=str, default="stdout",
                      help="Print censoring statistics (default: stdout).")

  return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.input:
        input_pattern = args.input
        output_directory_name = args.output
        output_directory = os.path.join(os.getcwd(), output_directory_name)
        os.makedirs(output_directory, exist_ok=True)
        readAllFiles()
        outputStats(args.stats)



