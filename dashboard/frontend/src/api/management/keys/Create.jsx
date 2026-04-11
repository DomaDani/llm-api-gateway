import api from "../../axios";

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
