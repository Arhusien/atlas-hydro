from flask import Response, jsonify


def repondre_succes(donnees: dict | list | None, code_statut: int | None = 200) -> tuple[Response, int]:
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
    return (
        jsonify(
            {
                "status": code_statut,
                "message": message,
            }
        ),
        code_statut,
    )
