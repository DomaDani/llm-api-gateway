import api from "../../axios";

export const fetchQuotaLimitTypes = async () => {
    try {
        const response = await api.get('quotas/limit-types')
        return response.data;
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch quota limit types');
    }
}

export const fetchQuotaPeriods = async () => {
    try {
        const response = await api.get('quotas/periods')
        return response.data;
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch quota periods');
    }
}

export const fetchQuotaInfos = async (projectId = null, userId = null, keyId = null, activeOnly = false) => {
    try {
        const response = await api.get('quotas/info', {
            project_id: projectId,
            user_id: userId,
            key_id: keyId,
            active_only: activeOnly,
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch quota information')
    }
}
