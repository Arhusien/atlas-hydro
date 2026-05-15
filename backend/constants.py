HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",  # noqa: E501
    # Empêcher la réception d'une réponse en cache
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
}

FORMATS_DATE = [
    "%Y/%m/%dT%H:%M:%SZ",
    "%Y/%m/%d %H:%M:%SZ",
    "%Y/%m/%dT%H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
]

URL_CENTRALES_HQ = (
    "https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/Donnees_VUE_CENTRALES_ET_OUVRAGES.json"
)
URL_SONDES_HQ = (
    "https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/Donnees_VUE_STATIONS_ET_TARAGES.json"
)

URL_ELECTRICITE_HQ = "https://donnees.solutions.hydroquebec.com/donnees-ouvertes/data/json/ges-electricite.json"

URL_GES_HQ = "https://donnees.hydroquebec.com/api/explore/v2.1/catalog/datasets/facteurges/records?limit=100"

FUSEAU_HORAIRE = "UTC"
TIMEOUT_REQUETE_SECONDES = 10
COOLDOWN_REQUETE_SECONDES = 3

DISTANCE_ASSOCIATION_CENTRALE_KM = 5
