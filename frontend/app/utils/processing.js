/**
 * Traite les relevés en les regroupant par type de donnée.
 * @param {Array} releves - La liste des relevés à traiter.
 * @returns {Object} Un objet contenant les relevés regroupés par type de donnée et triés par date.
 */
export function processReleves(releves) {
    let relevesByDataType = {};

    for (const releve of releves) {
        if (!relevesByDataType[releve.type_donnee]) {
            relevesByDataType[releve.type_donnee] = [];
        }
        relevesByDataType[releve.type_donnee].push(releve);
    }

    // Supprimer les relevés avec un type de donnée inconnu
    if (relevesByDataType["INCONNU"]) {
        delete relevesByDataType["INCONNU"];
    }

    // Trier les relevés en ordre alphabétique de type de donnée,
    // puis pour chaque type de donnée, trier les relevés par date décroissante
    relevesByDataType = Object.keys(relevesByDataType).sort().reduce((acc, key) => {
        acc[key] = relevesByDataType[key].sort((a, b) => new Date(b.date) - new Date(a.date));

        return acc;
    }, {});

    return relevesByDataType;
}
