from flask import Blueprint, jsonify

from extentions import cache
from services.carte_service import generer_geojson_installations
from utils import repondre_succes

bp_carte = Blueprint(
    name="carte",
    import_name=__name__,
    url_prefix="/api/carte",
)

TEMPS_CACHE_SECONDES = 60 * 60  # Une heure


@bp_carte.route("/installations", methods=["GET"])
@cache.cached(timeout=TEMPS_CACHE_SECONDES)
def afficher_geojson_installations():
    geojson_installations = generer_geojson_installations()

    return repondre_succes(geojson_installations, code_statut=200)
