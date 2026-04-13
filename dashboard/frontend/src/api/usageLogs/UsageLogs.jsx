import api from "../axios";

export const fetchUsageLogs = async(projectId, userId, aggregate, limit)  => {
    try {
        const response = await api.get('logs/info', {
            params: {
                project_id: projectId,
                user_id: userId,
                aggregate: aggregate,
                limit: limit
            }
        });
        return response.data;
    }
    catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch usage logs');
    }
}