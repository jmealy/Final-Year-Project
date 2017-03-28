import os
import re

def strip_newsgroup_header(text):
    """
    Given text in "news" format, strip the headers, by removing everything
    before the first blank line.
    """
    _before, _blankline, after = text.partition('\n\n')
    return after

_QUOTE_RE = re.compile(r'(writes in|writes:|wrote:|says:|said:'
                       r'|^In article|^Quoted from|^\||^>)')


def strip_newsgroup_quoting(text):
    """
    Given text in "news" format, strip lines beginning with the quote
    characters > or |, plus lines that often introduce a quoted section
    (for example, because they contain the string 'writes:'.)
    """
    good_lines = [line for line in text.split('\n')
                  if not _QUOTE_RE.search(line)]
    return '\n'.join(good_lines)


def strip_newsgroup_footer(text):
    """
    Given text in "news" format, attempt to remove a signature block.
    As a rough heuristic, we assume that signatures are set apart by either
    a blank line or a line made of hyphens, and that it is the last such line
    in the file (disregarding blank lines at the end).
    """
    lines = text.strip().split('\n')
    for line_num in range(len(lines) - 1, -1, -1):
        line = lines[line_num]
        if line.strip().strip('-') == '':
            break

    if line_num > 0:
        return '\n'.join(lines[:line_num])
    else:
        return text


def strip_digits(doc):
    return doc.translate(None, '0123456789')


data_path = '/home/james/PycharmProjects/final-year-project/working_data/20news-bydate-test/'


for dir in os.listdir(data_path):
    for fil in os.listdir(data_path + dir):
        with open(data_path + dir + '/' + fil, 'r+') as f:
            text = f.read()
            text = strip_newsgroup_header(text)
            text = strip_newsgroup_quoting(text)
            text = strip_newsgroup_footer(text)
            text = strip_digits(text)
            f.seek(0)
            f.write(text)
            f.truncate()

