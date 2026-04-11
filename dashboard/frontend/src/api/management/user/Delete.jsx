import api from "../../axios";

export const deleteUser = async (userId) => {
    try {
        const response = await api.delete('users/delete', {
            data: { user_id: userId },
        })
        return response.data
    } catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to delete user')
    }
}
