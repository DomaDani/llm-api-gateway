import api from "../../axios";

/**
 * Make a request to delete a user by id.
 *
 * @param {number} userId - User identifier.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
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
