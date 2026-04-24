from flask import Blueprint

from extentions import cache
from services.electricite_service import obtenir_donnees_electricite
from utils import repondre_erreur, repondre_succes

bp_electricite = Blueprint(
    name="electricite",
    import_name=__name__,
    url_prefix="/api/electricite",
)

TEMPS_CACHE_SECONDES = 60 * 15  # 15 minutes


@bp_electricite.route("/", methods=["GET"])
@cache.cached(timeout=TEMPS_CACHE_SECONDES)
def afficher_donnees_electricite():
    donnees_electricite = obtenir_donnees_electricite()
    if not donnees_electricite:
        return repondre_erreur("Les données reçues d'Hydro-Québec ne peuvent pas être traitées.", code_statut=502)

    return repondre_succes(donnees_electricite, code_statut=200)
