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
