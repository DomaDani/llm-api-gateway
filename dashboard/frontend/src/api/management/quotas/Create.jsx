import api from "../../axios"

/**
 * Make a request to create a new quota.
 *
 * @param {object} params - Quota creation parameters.
 * @param {number | null} params.project_id - Project identifier, or null for non-project quotas.
 * @param {number | null} params.user_id - User identifier, or null if not targeting a user.
 * @param {number | null} params.key_id - API key identifier, or null if not targeting a key.
 * @param {number} params.limit_id - Limit type identifier.
 * @param {number | null} params.limit_value - Numeric limit value.
 * @param {string} params.period - Quota period value.
 * @param {string | null} params.expires_at - Optional expiration timestamp.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
export const createQuota = async ({ project_id = null, user_id = null, key_id = null, limit_id, limit_value = null, period, expires_at = null }) => {
    try {
        const response = await api.post("quotas/create", {
            project_id,
            user_id,
            key_id,
            limit_id,
            limit_value,
            period,
            expires_at,
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || "Failed to create quota")
    }
}
