from flask import Blueprint

from extentions import cache
from services.carte_service import generer_geojson_installations, generer_geojson_regions
from utils import repondre_succes

bp_carte = Blueprint(
    name="carte",
    import_name=__name__,
    url_prefix="/api/carte",
)

TEMPS_CACHE_SECONDES_INSTALLATIONS = 60 * 60  # Une heure
TEMPS_CACHE_SECONDES_REGIONS = 24 * 60 * 60  # Un jour


@bp_carte.route("/installations", methods=["GET"])
@cache.cached(timeout=TEMPS_CACHE_SECONDES_INSTALLATIONS)
def afficher_geojson_installations():
    geojson_installations = generer_geojson_installations()

    return repondre_succes(geojson_installations, code_statut=200)


@bp_carte.route("/regions", methods=["GET"])
@cache.cached(timeout=TEMPS_CACHE_SECONDES_REGIONS)
def afficher_geojson_regions():
    geojson_regions = generer_geojson_regions()

    return repondre_succes(geojson_regions, code_statut=200)
