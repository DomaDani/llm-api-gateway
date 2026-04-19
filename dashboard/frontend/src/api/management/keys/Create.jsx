import api from "../../axios";

/**
 * Make a request to create a new API key.
 *
 * @param {object} params - API key creation parameters.
 * @param {number} params.project_id - Project identifier.
 * @param {string} params.name - API key label.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
export const createApiKey = async ({ project_id, name }) => {
    try {
        const response = await api.post('keys/create', {
            project_id,
            name,
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to create API key')
    }
}
