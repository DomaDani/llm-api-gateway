import api from "../../axios";

/**
 * Make a request to change the current user's email and username.
 *
 * @param {object} params - Identity change parameters.
 * @param {string} params.email - New email address.
 * @param {string} params.username - New username.
 * @returns {Promise<string>} A promise resolving to the success message.
 */
export async function changeIdentity({ email, username }) {
    try {
        const response = await api.put('/users/change-identity', {
            email,
            username
        });
        return response.data?.message || 'Identity updated successfully.';
    } catch (error) {
        const backendMessage = error?.response?.data?.detail

		throw new Error(backendMessage || 'Could not update identity. Please try again.')
    }
}