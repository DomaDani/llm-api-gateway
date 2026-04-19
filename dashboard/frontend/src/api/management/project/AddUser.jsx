import api from "../../axios";

/**
 * Make a request to add a user to a project.
 *
 * @param {object} params - Project membership parameters.
 * @param {number} params.project_id - Project identifier.
 * @param {number} params.user_id - User identifier.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
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
