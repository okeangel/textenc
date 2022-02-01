import os
import subprocess
from transliterate import translit
import csv


ALL_DRIVES = ["D:\\", "E:\\", "E:\\"]

BOOK_BASE_FOLDER = r"E:\books"

OKEAN_MUSIC_FOLDERS = [r"E:\YandexDisk\DJ",
                       r"E:\music"]
NATALIA_MUSIC_FOLDERS = [r"E:\Natalia\Google Диск\music active",
                         r"E:\Natalia\Music"]
IRYS_MUSIC_FOLDERS = [r"D:\YandexDisk\Irys Play",
                      r"D:\YandexDisk\Irys Music Cloud",
                      r"D:\Music Irys"]


def scan_file_types(folder):
    file_types = {}

    for root, dirs, files in os.walk(folder):
        for file in files:
            name, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext in file_types.keys():
                file_types[ext] += 1
            else:
                file_types[ext] = 1
    return file_types


def print_file_types(folder):
    types = scan_file_types(folder)
    for key in types.keys():
        print(f"{key}: {types[key]}")


def delete_junk(folders):
    junk_files = ['Thumbs.db', 'thumbs.db']
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file in junk_files:
                    print(f"{root} {file} 'junked!)")
                    os.remove(root + os.sep + file)
            """
            if not dirs and not files:
                if input(f"{root} 'empty! Remove? (Y/n)") == "Y":
                    os.rmdir(root)
                    print("Removed!")
            """


def permute_author_name(name):
    name = name.replace("_", " ")
    name = name.title()
    split_index = name.find(" ")
    name = name[:split_index] + "," + name[split_index:]
    return name


def rename_folders(folder):
    letter_dirs = list(filter(lambda x: not os.path.isdir(x),
                              os.listdir(path=folder)))
    print(letter_dirs)
    for d in letter_dirs:
        path = folder + "/" + d
        author_dirs = list(filter(lambda x: not os.path.isdir(x),
                                  os.listdir(path=path)))

        for author_dir in author_dirs:
            if "_" in author_dir:
                os.rename(path + os.sep + author_dir,
                          path + os.sep + permute_author_name(author_dir))


def pack_to_letters(folder):
    dirs = list(filter(lambda x: not os.path.isdir(x) and len(x) > 1,
                       os.listdir(path=folder)))
    for d in dirs:
        try:
            os.rename(folder + os.sep + d, folder + os.sep + d[0] + os.sep + d)
        except FileExistsError:
            pass


def correct_filename(folder):
    files = list(filter(lambda x: not os.path.isfile(x),
                        os.listdir(path=folder)))
    what = " - "
    for f in files:
        if what not in f and input(f"{f} ? (y/n)").lower() == "y":
            new_f = f.replace(". ", " - ", 1)
            print(new_f)


def pack_to_folders(folder):
    fdir = folder + os.sep + "!Детские"
    for file in os.listdir(path=fdir):
        if len(file) < 2:
            continue
        i = file.find(" - ")
        author = permute_author_name(file[:i]).strip()
        author_dir = os.path.join(folder, author[0], author)

        if not os.path.exists(author_dir):
            os.makedirs(author_dir)
        try:
            os.rename(fdir + os.sep + file,
                      author_dir + os.sep + file[i + 3:])
        except FileExistsError:
            author_dir = os.path.join(fdir, author[0], author)
            if not os.path.exists(author_dir):
                os.makedirs(author_dir)

            os.rename(fdir + os.sep + file,
                      os.path.join(author_dir, file[i + 3:]))


def translit_names(folder):
    fdir = os.path.join(folder, "0")
    for name in os.listdir(path=fdir):
        if os.path.isdir(os.path.join(fdir, name)):
            t_name = translit(name, 'ru')
            i = t_name.find(" ")
            t_name = t_name[:i] + "," + t_name[i:]
            os.rename(os.path.join(fdir, name),
                      os.path.join(fdir, t_name))


def unzip_all(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            name, ext = os.path.splitext(file)
            ext = ext.lower()
            print(root, file)
            if ext == ".zip":
                path_to_zip_file = os.path.join(root, file)
                path_to_7z = "C:\\Program Files\\7-Zip\\7z.exe"
                command = f"{path_to_7z} e {path_to_zip_file}"

                print(command)
                process = subprocess.Popen([path_to_7z, "x", path_to_zip_file,
                                           f"-o{root}", "-aoa"])
                process.wait()
                process.kill()
                os.remove(path_to_zip_file)


def csv_to_m3u(file_path):
    playlist = []

    with open(file_path, encoding="utf8") as csvfile:
        tracks = csv.DictReader(csvfile)
        for track in tracks:
            playlist.append(track['Folder'] + os.sep + track['Filename'] + '\n')

    with open(file_path + ".m3u8", "w+", encoding="utf8") as file:
        file.writelines(playlist)


if __name__ == "__main__":
    csv_to_m3u(r"C:\Users\okean\OneDrive\downloads\dupes okean.csv")
