import api from "../../axios"

/**
 * Make a request to create a new project.
 *
 * @param {object} params - Project creation parameters.
 * @param {string} params.name - Project name.
 * @param {number} params.manager_id - User id of the project manager.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
export const createProject = async ({ name, manager_id }) => {
    try {
        const response = await api.post("projects/create", {
            name,
            manager_id,
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || "Failed to create project")
    }
}