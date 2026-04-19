import api from "../../axios";

/**
 * Make a request to fetch the project information visible to the current user.
 *
 * @returns {Promise<any[]>} A promise resolving to the project list.
 */
export const fetchProjectInfosForUser = async () => {
    try {
        const response = await api.get('projects/info')
        return response.data;
    } catch (error) {
        const backendMessage = error.response?.data?.detail

        throw new Error(backendMessage || 'Failed to fetch project information');
    }
};