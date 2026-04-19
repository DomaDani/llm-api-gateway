import api from "../../axios";

/**
 * Make a request to fetch user information for a project or for the full user list.
 *
 * @param {number | null} projectId - Project identifier, or null for global user information.
 * @returns {Promise<any[]>} A promise resolving to the user information list.
 */
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
