import os
import sys
import threading
from pathlib import Path
from normalize import normalize

extensions = {
    "video": [".mp4", ".mov", ".avi", ".mkv"],
    "audio": [".mp3", ".wav", ".ogg", ".amr"],
    "images": [".jpg", ".png", ".jpeg", ".svg"],
    "python": [".py"],
    "drawings": [".dwg", ".dxf", ".ai"],
    "archives": [".zip", ".gz", ".tar", ".rar"],
    "documents": [
        ".pdf",
        ".txt",
        ".doc",
        ".docx",
        ".rtf",
        ".pptx",
        ".ppt",
        ".xlsx",
        ".xls",
    ],
}


def del_empty_dirs(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)
                print(a, "видалена")


def get_extension(file: Path) -> str:
    ext = file.suffix.lower()
    for key, values in extensions.items():
        if ext in values:
            return key
    return "unknown"


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    file.replace(new_name)


def sort_and_move_file(file: Path, root_dir: Path) -> None:
    extension = get_extension(file)
    move_file(file, root_dir, extension)


def sort_folder(path: Path) -> None:
    for elem in path.glob("**/*"):
        if elem.is_dir():
            if elem.stem in extensions.keys():
                continue
        if elem.is_file():
            thread = threading.Thread(
                target=sort_and_move_file, args=(elem, path))
            thread.start()


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        print("No path to folder")
        sys.exit(1)

    if not path.exists():
        print(f"Folder with path {path} doesn't exist.")
        sys.exit(1)

    sort_folder(path)
    del_empty_dirs(path)
    return "All done"


if __name__ == "__main__":
    print(main())
