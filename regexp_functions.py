import os
import re


def add_salt(match: re.Match) -> str:
    """
    Turn one found vowel into its "salty" form: vowel + "с" + the same vowel.

    Arguments:
    match: re.Match (a match object containing one vowel)

    Returns str (the vowel with the "с" + vowel insertion)
    """
    vowel = match.group()
    return vowel + "с" + vowel.lower()


def translate_to_salty(text: str) -> str:
    """
    Translate Russian text into the "salty language":
    after every vowel, insert the letter "с" followed by the same vowel.

    Arguments:
    text: str - source text in Russian

    Returns str - the text in the "salty language".
    """
    return re.sub(
        pattern=r"[аеёиоуыэюяАЕЁИОУЫЭЮЯ]",
        repl=add_salt,
        string=text,
    )


def get_chords(song_path: str) -> set[str]:
    """
    Find all guitar chords in a song file with lyrics and chords.

    Arguments:
    song_path: str - path to the song file

    Returns set[str] - unique chords found in the song.
    """
    with open(song_path, "r") as song_file:
        text = song_file.read()
    chords = re.findall(
        pattern=r"(?<!\w)[A-H][#b]?(?:m|maj|min|dim|aug|sus)?\d*(?:/[A-H][#b]?)?(?!\w)",
        string=text,
    )
    return set(chords)


def apply_sample_names(file_name: str, sample_names: dict[str, str]) -> str:
    """
    Replace sample names in a file name according to a dictionary.

    Arguments:
    file_name: str - file name to change
    sample_names: dict[str, str] - rules {old sample name: new sample name}

    Returns str - the file name with sample names replaced.
    """
    for old_name, new_name in sample_names.items():
        file_name = re.sub(
            pattern=rf"(?<![A-Za-z0-9]){re.escape(old_name)}(?![A-Za-z0-9])",
            repl=new_name,
            string=file_name,
        )
    return file_name


def make_new_file_name(
    file_name: str,
    pattern: str,
    new_pattern: str | None = None,
    sample_names: dict[str, str] | None = None,
) -> str:
    """
    Build a new file name: first replace the pattern, then the sample names.

    Arguments:
    file_name: str - original file name
    pattern: str - regular expression to replace
    new_pattern: str | None - replacement for the pattern; if None, no replacement
    sample_names: dict[str, str] | None - rules for renaming samples; if None, not applied

    Returns str - the new file name.
    """
    new_file_name = file_name
    if new_pattern is not None:
        new_file_name = re.sub(pattern, new_pattern, new_file_name)
    if sample_names is not None:
        new_file_name = apply_sample_names(new_file_name, sample_names)
    return new_file_name


def copy_file(source_path: str, destination_path: str) -> None:
    """
    Copy a file: read the source file and write its content to a new file.

    Arguments:
    source_path: str - path to the original file
    destination_path: str - path to the new file

    Returns None.
    """
    with open(source_path, "rb") as source, open(destination_path, "wb") as destination:
        destination.write(source.read())


def rename_files(
    dir: str,
    pattern: str,
    new_pattern: str | None = None,
    sample_names: dict[str, str] | None = None,
    to_replace: bool = False,
) -> None:
    """
    Rename files in a directory by a pattern and/or by a dictionary of sample names.

    Arguments:
    dir: str - directory with the files
    pattern: str - regular expression used to select files (and replaced by new_pattern)
    new_pattern: str | None - replacement for the pattern; if None, only selects files
    sample_names: dict[str, str] | None - rules {old sample name: new sample name},
        applied after the pattern replacement
    to_replace: bool - True to rename (originals are removed),
        False to copy (originals are kept); False by default

    Returns None.
    """
    for file_name in os.listdir(dir):
        if re.search(pattern, file_name) is None:
            continue
        new_file_name = make_new_file_name(file_name, pattern, new_pattern, sample_names)
        if new_file_name == file_name:
            continue
        old_path = os.path.join(dir, file_name)
        new_path = os.path.join(dir, new_file_name)
        if to_replace:
            os.rename(old_path, new_path)
        else:
            copy_file(old_path, new_path)