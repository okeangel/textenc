"""A tool for mass converting text files from an unknown encoding
to standard.
"""

import re
import shutil
import winsound

import engine


def signal():
    """Make beeps when user input is needed."""
    winsound.Beep(440, 200)
    winsound.Beep(880, 200)
    winsound.Beep(1760, 300)
    winsound.Beep(880, 100)
    winsound.Beep(1760, 400)


def replace_chars(text, encoding):
    # TODO: она не срабатывает! заставь её делать замены
    text = re.sub('\x1A', '-', text)
    text = re.sub('\x00', '', text)
    if encoding == 'IBM866':
        text = re.sub('ў', 'ё', text)
        text = re.sub('\r\n\f\r\n *- [0-9]* -\r\n\r\n', '\r\n', text)
        text = re.sub('\r\n *[0-9]*\r\n\f\r\n', '\r\n', text)
        text = re.sub('\r\n\f\r\n', '\r\n', text)
    # TODO: replace \r[not\n] to \r\n
    # TODO: replace [not\r]\n to \r\n
    return text


def correct(base_path, file_paths):
    auto = {}

    for path in file_paths:        
        encoding, confidence, raw_text = engine.detect_encoding(path)
        text = replace_chars(raw_text, encoding)

        if encoding == engine.STANDARD:
            continue

        if encoding in auto:
            if confidence >= auto[encoding].get('all', 2):
                save(base_path, path, text)
                continue
            elif confidence <= auto[encoding].get('leave', -1):
                continue

        print('\n\n' + ' =' * 39 + '\n')
        print(f'"{text[:1000]}..."')
        print(f'File name: "{path}".')
        print(f'Confidence: {confidence}.')
        print(f'Enc: {encoding}.\n')
        signal()
        
        request = 'Convert (C) / No (N)/ All above (A)/ No below (L)? '
        command = input(request).lower()

        while True:
            if command == 'c':
                save(base_path, path, text)
                break
            elif command == 'n':
                break
            elif command == 'a':
                save(base_path, path, text)
                if encoding in auto:
                    auto[encoding]['all'] = confidence
                else:
                    auto[encoding] = {'all': confidence}
                break
            elif command == 'l':
                if encoding in auto:
                    auto[encoding]['leave'] = confidence
                else:
                    auto[encoding] = {'leave': confidence}
                break
            else:
                message = 'Unrecognized command. Please enter a valid one: '
                command = input(message).lower()


def save(base, path, text):
    rel_path = path.relative_to(base)
    backup_path = base.parent.joinpath(base.name + '_filenc_backup', rel_path)

    if not backup_path.parent.exists():
        backup_path.parent.mkdir(parents=True)
    shutil.move(path, backup_path)
    
    path.write_bytes(text.encode())


def main():
    engine.welcome()
    file_paths = engine.get_file_paths()
    correct(engine.BASE_PATH, file_paths)

   
if __name__ == "__main__":
    main()
