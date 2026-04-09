import api from "../../axios";

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