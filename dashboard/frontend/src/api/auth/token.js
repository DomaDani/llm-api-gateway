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

export function getTokenExpiryMs(token) {
    const payload = decodeJwtPayload(token)

    if (!payload?.exp) {
        return null
    }

    return payload.exp * 1000
}

export function isTokenExpired(token) {
    const expiryMs = getTokenExpiryMs(token)

    if (!expiryMs) {
        return true
    }

    return expiryMs <= Date.now()
}
