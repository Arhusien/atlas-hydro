from flask import Blueprint

from extentions import cache
from services.installations_service import obtenir_installation
from utils import repondre_erreur, repondre_succes

bp_installations = Blueprint(
    name="installations",
    import_name=__name__,
    url_prefix="/api/installations",
)

TEMPS_CACHE_SECONDES = 60  # Une minute


@bp_installations.route("/<string:id_installation>", methods=["GET"])
@cache.cached(timeout=TEMPS_CACHE_SECONDES)
def afficher_installation(id_installation: str):
    installation = obtenir_installation(id_installation)
    if not installation:
        return repondre_erreur("Installation introuvable", code_statut=404)

    return repondre_succes(installation, code_statut=200)
