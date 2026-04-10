import api from "../../axios";

export const fetchProjectInfosForUser = async () => {
    try {
        const response = await api.get('projects/info')
        return response.data;
    } catch (error) {
        const backendMessage = error.response?.data?.detail

        throw new Error(backendMessage || 'Failed to fetch project information');
    }
};