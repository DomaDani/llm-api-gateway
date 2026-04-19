import api from "../../axios";

/**
 * Make a request to fetch API keys for a project or a user.
 *
 * @param {number | null} projectId - Project identifier, or null to skip project scope.
 * @param {number | null} userId - User identifier, or null to skip user scope.
 * @returns {Promise<any[]>} A promise resolving to the API key list.
 */
export const fetchKeyInfos = async (projectId = null, userId = null) => {
    try {
        const response = await api.get('keys/info', {
            params: {
                project_id: projectId,
                user_id: userId,
            },
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch key information')
    }
}