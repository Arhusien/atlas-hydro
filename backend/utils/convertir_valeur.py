from typing import Any


def convertir_valeur(valeur: str | int | float | bool, type_cible: type, valeur_par_defaut: Any | None = None) -> Any:
    """
    Convertit une valeur en un type cible.

    Parameters:
        valeur (str | int | float | bool): La valeur à convertir.
        type_cible (type): Le type cible.
        valeur_par_defaut (Any, optionel): La valeur par défaut si la conversion échoue. Par défaut None.

    Returns:
        (Any): La valeur convertie ou la valeur par défaut.
    """

    try:
        # Convertir la valeur dans le type cible
        valeur = type_cible(valeur)

    except (ValueError, TypeError):
        # Si la valeur n'a pas pu être convertie, retourner la valeur par défaut
        return valeur_par_defaut

    # Sinon, retourner la valeur convertie
    return valeur
