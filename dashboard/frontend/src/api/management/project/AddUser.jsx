import api from "../../axios";

export const addUserToProject = async ({ project_id, user_id }) => {
    try {
        const response = await api.post('projects/add-user', {
            project_id,
            user_id,
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to add user to project')
    }
}
