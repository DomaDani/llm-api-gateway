import api from "../../axios";

/**
 * Make a request to remove a user from a project.
 *
 * @param {object} params - Project membership parameters.
 * @param {number} params.project_id - Project identifier.
 * @param {number} params.user_id - User identifier.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
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
