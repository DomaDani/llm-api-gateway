import api from "../../axios"

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
