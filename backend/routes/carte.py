from flask import Blueprint, jsonify

from extentions import cache
from services.carte_service import generer_geojson_installations

bp_carte = Blueprint(
    name="carte",
    import_name=__name__,
    url_prefix="/api/carte",
)

TEMPS_CACHE_SECONDES = 60 * 60  # Une heure


@bp_carte.route("/installations", methods=["GET"])
@cache.cached(timeout=TEMPS_CACHE_SECONDES)
def obtenir_geojson_installations():
    geojson_installations = generer_geojson_installations()

    return jsonify(geojson_installations), 200
