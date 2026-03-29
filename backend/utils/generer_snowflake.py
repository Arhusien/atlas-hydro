from datetime import datetime, timezone

from snowflake import SnowflakeGenerator

# Utiliser le 1er janvier 2026 comme point de départ
epoch = datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp()
epoch = int(epoch * 1000)

generateur_id = SnowflakeGenerator(instance=1, epoch=int(epoch))


def generer_snowflake() -> int:
    """
    Génère un identifiant snowflake.

    Returns:
        (int): Un identifiant snowflake.
    """

    return next(generateur_id)
