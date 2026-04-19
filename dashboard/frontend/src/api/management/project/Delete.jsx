import api from "../../axios"

/**
 * Make a request to delete a project by id.
 *
 * @param {number} projectId - Project identifier.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
export const deleteProject = async (projectId) => {
    try {
        const response = await api.delete("projects/delete", {
            data: { project_id: projectId },
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || "Failed to delete project")
    }
}
