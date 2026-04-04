HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",  # noqa: E501
    # Empêcher la réception d'une réponse en cache
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
}

URL_API_DONNEES_HQ = "https://donnees.hydroquebec.com/api/explore/v2.1/catalog/datasets"

URL_CENTRALES_HQ = (
    "https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/Donnees_VUE_CENTRALES_ET_OUVRAGES.json"
)
URL_SONDES_HQ = (
    "https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/Donnees_VUE_STATIONS_ET_TARAGES.json"
)

FUSEAU_HORAIRE = "America/Toronto"
LIMITE_ELEMENTS_API = 100
TIMEOUT_REQUETE_SECONDES = 10
PAUSE_ENTRE_REQUETES_SECONDES = 3

DISTANCE_ASSOCIATION_CENTRALE_KM = 5
