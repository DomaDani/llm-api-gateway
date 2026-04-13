import api from "../../axios";

export const fetchUserInfos = async (projectId = null) => {
    try {
        const params = projectId != null ? { project_id: projectId } : {};
        const response = await api.get('users/info', { params });
        return response.data;
    } catch (error) {
        const backendMessage = error.response?.data?.detail

        throw new Error(backendMessage || 'Failed to fetch user information');
    }
};
