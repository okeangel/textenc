"""A tool for mass converting text files from an unknown encoding
to standard.
"""

import pathlib
import shutil

import chardet


with open('settings_base_path.txt', encoding='utf-8') as file:
    text = file.read()
    if text.endswith('\n'):
        text = text[:-1]
    BASE_PATH = pathlib.Path(text)


STANDARD = 'utf-8'


eng = 'qwertyuiopasdfghjklzxcvbnm'
ru = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
digits = '1234567890'
LETTERS = set(eng + eng.upper() + ru + ru.upper() + digits)


def detect_encoding(file_path):
    """Detect encoding and return encoding, confidence level and decoded text.
    """

    blob = file_path.read_bytes()
    detection = chardet.detect(blob)
    
    encoding = detection["encoding"]
    confidence = detection["confidence"]
    if encoding:
        if encoding == 'MacCyrillic':
            encoding = 'windows-1251'
        try:
            text = blob.decode(encoding)
        except UnicodeDecodeError as message:
            print(f' - - - V V V {message} V V V - - -')
            print(f'{confidence:<18} {encoding:<12} {file_path}')
            text = ''
    else:
        text = ''

    return encoding, confidence, text


def get_file_paths(suffix='txt'):
    return list(BASE_PATH.glob(f'**/*.{suffix}'))


def welcome():
    with open('welcome.txt') as file:
        print(file.read())
