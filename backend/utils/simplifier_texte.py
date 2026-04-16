import re
import unicodedata
from typing import Optional

REGEX_ALPHANUMERIQUES = re.compile(r"[^a-z0-9]")


def simplifier_texte(texte: str) -> Optional[str]:
    """
    Simplfie une chaîne de caractères.

    Parameters:
        texte (str): La chaîne de caractères à simplifier.

    Returns:
        (Optional[str]): La chaîne de caractères simplifiée ou une valeur nulle.
    """

    if not isinstance(texte, str):
        return None

    # Simplifier la chaîne de caractères
    texte = texte.lower().replace("œ", "oe")
    texte = unicodedata.normalize("NFKD", texte).encode("ASCII", "ignore").decode("utf-8")

    # Conserver les caractères alphanumériques
    return re.sub(REGEX_ALPHANUMERIQUES, "", texte)
