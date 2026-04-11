import api from "../../axios"

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
