/**
 * Decode the payload section of a JWT.
 *
 * @param {string} token - JWT string.
 * @returns {object | null} The decoded payload or null if decoding fails.
 */
function decodeJwtPayload(token) {
    try {
        const [, payload] = token.split('.')
        if (!payload) {
            return null
        }

        const normalizedPayload = payload.replace(/-/g, '+').replace(/_/g, '/')
        const paddedPayload = normalizedPayload + '='.repeat((4 - (normalizedPayload.length % 4)) % 4)

        return JSON.parse(atob(paddedPayload))
    } catch {
        return null
    }
}

/**
 * Get the expiration time of a JWT in milliseconds since epoch.
 *
 * @param {string} token - JWT string.
 * @returns {number | null} The expiration timestamp in milliseconds, or null if unavailable.
 */
export function getTokenExpiryMs(token) {
    const payload = decodeJwtPayload(token)

    if (!payload?.exp) {
        return null
    }

    return payload.exp * 1000
}

/**
 * Check whether a JWT is expired.
 *
 * @param {string} token - JWT string.
 * @returns {boolean} True if the token is expired or invalid.
 */
export function isTokenExpired(token) {
    const expiryMs = getTokenExpiryMs(token)

    if (!expiryMs) {
        return true
    }

    return expiryMs <= Date.now()
}
