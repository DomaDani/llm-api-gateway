import api from "../../axios";

/**
 * Make a request to delete a quota by id.
 *
 * @param {number} id - Quota identifier.
 * @returns {Promise<any>} A promise resolving to the backend response data.
 */
export const deleteQuota = async (id) => {
	try {
		const response = await api.delete('quotas/delete', {
			data: { id },
		})
		return response.data
	} catch (error) {
		const backendMessage = error.response?.data?.detail
		throw new Error(backendMessage || 'Failed to delete quota')
	}
}
