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