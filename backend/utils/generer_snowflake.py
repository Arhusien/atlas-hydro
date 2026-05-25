import time
from datetime import datetime, timezone

from snowflake import SnowflakeGenerator

# Définir le point de référence temporel des identifiants
epoch = datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp()
epoch = int(epoch * 1000)

generateur_id = SnowflakeGenerator(instance=1, epoch=epoch)


def generer_snowflake() -> int:
    """
    Génère un identifiant snowflake.

    Returns:
        (int): Un identifiant snowflake.
    """

    id = next(generateur_id)

    if id is not None:
        return id
    # Si plus de 4096 identifiants ont été générés dans la même milliseconde
    else:
        # Récupérer la milliseconde actuelle
        ms_actuelle = time.time_ns() // 1000000

        # Boucler jusqu'à ce que cette milliseconde soit dépassée
        while (time.time_ns() // 1000000) <= ms_actuelle:
            pass

        # Générer un nouvel identifiant
        return next(generateur_id)
