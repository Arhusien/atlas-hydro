from flask import Response, jsonify


def repondre_succes(donnees: dict | list | None, code_statut: int | None = 200) -> tuple[Response, int]:
    """
    Retourne une réponse HTTP 2XX avec un dictionnaire ou une liste de données.

    Parameters:
        donnees (dict | list): Le dictionnaire ou la liste de données à retourner.
        code_statut (int, optionel): Le code statut de la réponse.

    Returns:
        (tuple[Response, int]): Un tuple contenant la réponse HTTP et le code statut.
    """

    return (
        jsonify(
            {
                "status": code_statut,
                "data": donnees if donnees is not None else {},
            }
        ),
        code_statut,
    )


def repondre_erreur(message: str | None = "Erreur interne", code_statut: int | None = 500) -> tuple[Response, int]:
    """
    Retourne une réponse HTTP 4XX/5XX avec un message d'erreur.

    Parameters:
        message (str, optionel): Le message d'erreur à retourner.
        code_statut (int, optionel): Le code statut de la réponse.

    Returns:
        (tuple[Response, int]): Un tuple contenant la réponse HTTP et le code statut.
    """

    return (
        jsonify(
            {
                "status": code_statut,
                "message": message,
            }
        ),
        code_statut,
    )
