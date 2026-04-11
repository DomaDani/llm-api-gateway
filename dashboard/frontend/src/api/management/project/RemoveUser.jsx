import api from "../../axios";

export const removeUserFromProject = async ({ project_id, user_id }) => {
    try {
        const response = await api.post('projects/remove-user', {
            project_id,
            user_id,
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to remove user from project')
    }
}
