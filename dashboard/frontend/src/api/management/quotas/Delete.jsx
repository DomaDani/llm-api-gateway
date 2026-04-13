import api from "../../axios";

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
