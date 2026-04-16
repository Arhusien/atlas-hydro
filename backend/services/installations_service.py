from typing import Optional

from db import db
from models import Installation


def obtenir_installation(id_installation: str) -> Optional[dict]:
    installation = db.session.get(Installation, id_installation)

    if not installation:
        return None

    return installation.serialiser(avec_releves=True)
