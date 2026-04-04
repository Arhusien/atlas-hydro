from models import Installation


def generer_geojson_installations() -> dict:
    """
    Récupère toutes les installations d'Hydro-Québec et génère un objet GeoJSON.

    Returns:
        (dict): Un objet GeoJSON conteant les points de toutes les installations.
    """

    lst_installations: list[Installation] = Installation.query.all()
    lst_points_installations = []

    for installation in lst_installations:
        donnees_installation = installation.serialiser()

        lst_points_installations.append(
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
                    "centrale_id": donnees_installation.get("centrale_id", None),
                },
            },
        )

    return {
        "type": "FeatureCollection",
        "features": lst_points_installations,
    }
