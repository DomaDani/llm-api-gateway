import api from "../../axios";

/**
 * Make a request to delete an API key by id.
 *
 * @param {number} keyId - API key identifier.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
export const deleteApiKey = async (keyId) => {
    try {
        const response = await api.delete('keys/delete', {
            data: { key_id: keyId },
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to delete API key')
    }
}
