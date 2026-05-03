import {
    decimalToSexagesimal,
} from "geolib";
import {
    DateTime,
} from "luxon";

/**
 * Convertit une coordonnée décimale au format degrés minutes et secondes avec indication de direction.
 * @param {number} coord - La coordonnée décimale à convertir.
 * @param {boolean} isLat - Si la coordonnée est une latitude.
 * @returns {string | null} La coordonnée au format degrés minutes et secondes.
 */
export function convertToDMS(coord, isLat) {
    if (typeof coord !== "number") return null;

    const dms = decimalToSexagesimal(Math.abs(coord)).replace(/\s/g, ""),
        direction = isLat
            ? (coord >= 0 ? "N" : "S")
            : (coord >= 0 ? "E" : "W");

    return `${dms}${direction}`;
}

/**
 * Formate une date dans un fuseau horaire cible.
 * @param {string} utcDate - La date au format ISO et sous le fuseau horaire universel.
 * @param {string} timezone - Le fuseau horaire cible.
 * @param {any} options - Les options de formatage supplémentaires.
 * @returns {string} La date formatée.
 */
export function formatToLocalDate(utcDate, timezone, options = {}) {
    return DateTime.fromISO(utcDate, {
        zone: "utc",
    })
        .setZone(timezone)
        .toLocaleString({
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            ...options,
        });
}
