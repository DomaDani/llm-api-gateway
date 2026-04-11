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
