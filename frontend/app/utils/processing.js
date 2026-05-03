export function processReleves(releves) {
    let relevesByDataType = {};

    for (const releve of releves) {
        if (!relevesByDataType[releve.type_donnee]) {
            relevesByDataType[releve.type_donnee] = [];
        }
        relevesByDataType[releve.type_donnee].push(releve);
    }

    if (relevesByDataType["INCONNU"]) {
        delete relevesByDataType["INCONNU"];
    }

    relevesByDataType = Object.keys(relevesByDataType).sort().reduce((acc, key) => {
        acc[key] = relevesByDataType[key].sort((a, b) => new Date(b.date) - new Date(a.date));

        return acc;
    }, {});

    return relevesByDataType;
}
