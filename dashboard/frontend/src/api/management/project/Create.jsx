import api from "../../axios"

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