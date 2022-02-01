"""A tool for mass converting text files from an unknown encoding
to standard.
"""

import csv
import datetime
import multiprocessing

from collections import Counter
from time import time

import engine


FTIME = datetime.datetime.now().strftime('%y%m%d-%H%M%S')


with open('chars.csv', encoding='utf-8', newline='') as csvfile:
    char_reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    next(char_reader)

    # short names have length more than 1 symbol, let filter it
    NP_MAP = {
        chr(int(row[0])): row[3] for row in char_reader if len(row[3]) > 1
    }


def survey_file(filename):
    encoding, confidence, text = engine.detect_encoding(filename)
    char_counter = Counter()
    for char, count in Counter(text).items():
        if char not in engine.LETTERS:
            char_counter[char] = count
    return confidence, encoding, filename, char_counter


def update_nonprintable_keys(counter):
    chars = list(counter.keys())
    for char in chars:
        if char in NP_MAP:
            symbol = NP_MAP[char]
            counter[symbol] = counter.pop(char)


def get_summary(base_path, file_paths):
    summary = []
    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
        summary.extend(pool.map(
            survey_file,
            file_paths,
        ))

    total_char_counts = Counter()
    summary_dicts = []

    for row in summary:
        counter = row[3]
        update_nonprintable_keys(counter)
        total_char_counts += counter
        counter['confidence'] = row[0]
        counter['encoding'] = row[1]
        counter['file name'] = row[2]
        summary_dicts.append(counter)

    all_used_chars = sorted(total_char_counts.keys())

    header = [
        'confidence',
        'encoding',
        *all_used_chars,
        'file name',
    ]
    
    save_counter(total_char_counts, f'reports/{FTIME}_total_chars.csv')
    save_summary_dicts(summary_dicts, header, f'reports/{FTIME}_summary.csv')


def save_summary_dicts(summary, fieldnames, name):
    with open(name, 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_NONNUMERIC
        )
        writer.writeheader()
        for row in summary:
            writer.writerow(row)


def save_counter(counter, name):
    with open(name, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for char in sorted(counter.keys()):
            writer.writerow([
                # ord(key),
                # f'{ord(key):X}',
                char,
                counter[char],
            ])


def main():
    start = time()
    
    file_paths = engine.get_file_paths()
    get_summary(engine.BASE_PATH, file_paths)
    
    result = round(time() - start)
    with open(f'reports/{FTIME}_execution_time_{result}_seconds.txt', 'w') as file:
        file.write('')


if __name__ == "__main__":
    main()
