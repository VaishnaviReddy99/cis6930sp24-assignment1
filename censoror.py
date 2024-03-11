import sys
import argparse
import os
import string
import spacy
import shutil
import re
import glob
from spacy.matcher import Matcher
from spacy_download import load_spacy
import nltk

# Download stopwords (if not already downloaded)
nltk.download('stopwords')


# Define the output directory name
output_directory_name = 'output'
unicode_char = '\u2588'
statsOP = []
input_pattern = ".txt"
nlp = load_spacy("en_core_web_sm")

stop_words = nltk.corpus.stopwords.words('english')

def extract_entities(text):
    matcher = Matcher(nlp.vocab)
    name_pattern = [
        # Option 1: First Name, Last Name (with punctuation)
        [
            # Option 1: More strict name with punctuation
            {"POS": "PROPN"},  # Must be a proper noun
            {"POS": "PROPN"} | {"ORTH": {"IN": [".", ",", "-"]}}  # Last name can have punctuation
        ],
            # Option 2: Full Name (with punctuation)
        [{"ORTH": {"IN": [".", ",", "-"]}}, {"POS": "PROPN"}],  # Allow punctuation within or at the beginning of a name
        # Option 3: Initials with Last Name (with punctuation)
    ]


    address_pattern = [
        [{"LIKE_NUM": True}, {"ORTH": {"IN": ["St", "Rd", "Ave", "Ln", "Blvd"]}} ],       [{"POS": "PROPN", "OP": "+"}],  # City (at least one proper noun)
        [{"POS": "PROPN"} | {"POS": "GPE"}],  # Optional state or geopolitical entity
        [{"POS": "NUM", "LENGTH": 5}]  # Pincode (5 digits)
    ]

    matcher.add("PERSON",name_pattern)
    matcher.add("ADDRESS", address_pattern)

    doc = nlp(text)
    matches = matcher(doc)
    entities = []
    for label, start, end,  in matches:
        span = doc[start:end]
        entities.append((label, span.text))
    return entities

def mask_phone_numbers(text):
    # Define a regular expression pattern for matching phone numbers
    local_pattern = re.compile(r'^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
    # Replace phone numbers with '**'
    pattern = r"\b\d{3} \d{3} \d{4}\b"
    phone_num = unicode_char*3+" "+unicode_char*3+" "+unicode_char*4
    masked_text = re.sub(local_pattern, unicode_char*11, text)
    masked_text = re.sub(pattern, phone_num, text)
    masked = False
    if unicode_char in masked_text : masked = True
    return masked, masked_text


def replace_dates(text):
  """
  Replaces dates in text with an asterisk (*) followed by the length of the date entity.
  """
  doc = nlp(text)
  dates= []
  count = 0
  for ent in doc.ents:
      if ent.label_ == "DATE":
          dates.append(ent.text)
  for date in dates:
      if checkForStopWord(date):
          continue
      text.replace(date, unicode_char*len(date))
      count = count + 1

  return text,count

def preprocess_text(text):
    punc_to_remove = r'[!"#$%&\'()*+,./:;<=>?@\\^`{|}~_-]'  # Characters to remove
    preprocessed_text = re.sub(punc_to_remove, ' ', text)
    return preprocessed_text
def censor_text(filename, text):
    preprocossedtext = preprocess_text(text)
    entities = extract_entities(preprocossedtext)
    result_str = text
    count = 0
    stop_recog = 0
    for label, entity_text in entities:
        entity_words = entity_text.split(" ")
        for entity_word in entity_words:
            if checkForStopWord(entity_word) :
                stop_recog = stop_recog +1
                continue
            result_str = result_str.replace(entity_word,unicode_char*len(entity_word))
            count = count + 1


    masked, result_str = mask_phone_numbers(result_str)
    phone_masked = 0
    if masked : phone_masked = 1

    result_str,date_count = replace_dates(result_str)
    statsOP.append("File : " + filename+" \nNo.of words censored : " + str(count)+" \nNo.of phone numbers masked : "+str(phone_masked)+"\nNo.of dates masked: "+str(date_count))
    return result_str

def checkForStopWord(word):

    if word in stop_words or word in ["X", "Graduate", "Date", "Month","Origin","Filename","Content"]:
        return True
    return False

def readAllFiles():
    # Iterate through all folders, subfolders, and files recursively
    full_pattern = os.path.join(os.getcwd(), '**', input_pattern)
    matching_files = glob.glob(full_pattern, recursive=True)

    for file in matching_files:
        destination_path = os.path.join(output_directory, os.path.basename(file)+".censored")
        # Read the content of the file
        with open(file, 'r', encoding='utf-8') as file_content:
            content = file_content.read()

        # Apply your transformation to the content (e.g., add some text)
        transformed_content = censor_text(file, content)
        # Write the transformed content to the destination file
        with open(destination_path, 'w', encoding='utf-8') as destination_file:
            destination_file.write(transformed_content)



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
