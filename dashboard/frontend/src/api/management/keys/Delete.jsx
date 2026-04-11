import api from "../../axios";

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
