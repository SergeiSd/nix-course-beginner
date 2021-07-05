"""This modelu provides the function to converts all sentences to uppercase."""
import argparse
import codecs
import os
import sys
import nltk
# nltk.download('punkt')

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_file', default='strings.txt',
                    help='The location of file.')
args = parser.parse_args()


def get_strings(file: str = args.path_file) -> list:
    """Reading data from a file and converting it to a list of sentences.

    Parameters
    ----------
      - file: `str`
      
          The path to the data file.
      
    Returns
    -------
        a list of sentences.
    """

    if not os.path.isfile(file):
        print("Error: {} does not exist.".format(file))
        sys.exit(1)

    with codecs.open(file, 'r', encoding='utf8') as reader:
        content = reader.read()

    sents = nltk.sent_tokenize(content)
    return sents


def upper(sents: list = get_strings()) -> list:
    """Converts all sentences to uppercase.

    Parameters
    ----------
      - sents: `list`
      
          Text sentences.
      
    Returns
    -------
        a list of uppercase sentences.
    """

    return [x.upper() for x in sents if 'price' in x]


if __name__ == '__main__':
    for index, line in enumerate(upper()):
        print(f'{index+1} line:', line)
