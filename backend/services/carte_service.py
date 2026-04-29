import geopandas as gpd
import pandas as pd

from models import Installation


def generer_geojson_installations() -> dict:
    """
    Récupère toutes les installations d'Hydro-Québec et génère un objet GeoJSON.

    Returns:
        (dict): Un dictionnaire GeoJSON contenant les points de toutes les installations.
    """

    lst_installations: list[Installation] = Installation.query.all()

    points_installations_par_types = {}
    for installation in lst_installations:
        type_nom = installation.type.value

        if type_nom not in points_installations_par_types:
            points_installations_par_types[type_nom] = {
                "type": "FeatureCollection",
                "features": [],
            }

        donnees_installation = installation.serialiser()

        points_installations_par_types[type_nom]["features"].append(
            {
                "type": "Feature",
                "id": donnees_installation["id"],
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        donnees_installation["x"],
                        donnees_installation["y"],
                        donnees_installation["z"],
                    ],
                },
                "properties": {
                    "objectid": donnees_installation["id"],
                    "nom": donnees_installation["nom"],
                    "type": donnees_installation["type"],
                    "region": {
                        "code": donnees_installation["code_region"],
                        "nom": donnees_installation["nom_region"],
                    },
                    "ouvrage_id": donnees_installation.get("ouvrage_id", None),
                },
            }
        )

    return points_installations_par_types


def generer_geojons_regions() -> dict:
    """
    Récupère les régions dans lesquelles opère Hydro-Québec et génère un objet GeoJSON.

    Returns:
        (dict): Un dictionnaire GeoJSON contenant les régions du réseau d'Hydro-Québec.
    """

    # Récupérer les frontières internes des États-Unis
    url_us = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    regions_us = gpd.read_file(url_us)

    # Récupérer les frontières de New York
    new_york = regions_us[regions_us["name"] == "New York"].copy()
    new_york["region"] = "NewYork"

    # Liste des états de la Nouvelle-Angleterre
    etats_na = [
        "Maine",
        "New Hampshire",
        "Vermont",
        "Massachusetts",
        "Rhode Island",
        "Connecticut",
    ]
    nouvelle_angleterre = regions_us[regions_us["name"].isin(etats_na)].copy()
    nouvelle_angleterre["region"] = "NewEngland"

    # Fusionner les frontières des états de la Nouvelle-Angleterre
    nouvelle_angleterre = nouvelle_angleterre.dissolve(by="region").reset_index()

    # Récupérer les frontières internes du Canada
    url_canada = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/canada.geojson"
    regions_ca = gpd.read_file(url_canada)

    provinces_ca = regions_ca[
        regions_ca["name"].isin(
            [
                "Quebec",
                "Ontario",
                "New Brunswick",
            ]
        )
    ].copy()

    # Uniformiser le nom de la colonne
    provinces_ca = provinces_ca.rename(columns={"name": "region"})
    provinces_ca["region"] = provinces_ca["region"].str.replace(" ", "")

    # Combiner les données en un seul objet
    donnees_regions = pd.concat(
        [
            new_york[["region", "geometry"]],
            nouvelle_angleterre[["region", "geometry"]],
            provinces_ca[["region", "geometry"]],
        ]
    )

    regions = gpd.GeoDataFrame(donnees_regions, geometry="geometry").to_geo_dict()

    return regions
