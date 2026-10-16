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