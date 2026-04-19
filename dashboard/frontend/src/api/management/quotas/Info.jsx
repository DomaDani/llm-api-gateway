import api from "../../axios";

/**
 * Make a request to fetch available quota limit types.
 *
 * @returns {Promise<any[]>} A promise resolving to the limit type list.
 */
export const fetchQuotaLimitTypes = async () => {
    try {
        const response = await api.get('quotas/limit-types')
        return response.data;
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch quota limit types');
    }
}

/**
 * Make a request to fetch available quota periods.
 *
 * @returns {Promise<any[]>} A promise resolving to the period list.
 */
export const fetchQuotaPeriods = async () => {
    try {
        const response = await api.get('quotas/periods')
        return response.data;
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch quota periods');
    }
}

/**
 * Make a request to fetch quotas for a project, user, or API key.
 *
 * @param {number | null} projectId - Project identifier.
 * @param {number | null} userId - User identifier.
 * @param {number | null} keyId - API key identifier.
 * @param {boolean} activeOnly - Whether to include only active quotas.
 * @param {boolean} includeInherited - Whether to include inherited quotas.
 * @returns {Promise<any[]>} A promise resolving to the quota list.
 */
export const fetchQuotaInfos = async (projectId = null, userId = null, keyId = null, activeOnly = false, includeInherited = true) => {
    try {
        const response = await api.get('quotas/info', {
            params: {
                project_id: projectId,
                user_id: userId,
                key_id: keyId,
                active_only: activeOnly,
                include_inherited: includeInherited,
            }
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch quota information')
    }
}
