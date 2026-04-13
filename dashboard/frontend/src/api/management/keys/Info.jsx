import api from "../../axios";

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