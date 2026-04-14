import api from "../axios";

export const fetchUsageLogs = async(projectId, userId, aggregate, limit, offset = 0)  => {
    try {
        const response = await api.get('logs/info', {
            params: {
                project_id: projectId,
                user_id: userId,
                aggregate: aggregate,
                limit: limit,
                offset: offset,
            }
        });
        return response.data;
    }
    catch (error) {
        const backendMessage = error.response?.data?.detail
        throw new Error(backendMessage || 'Failed to fetch usage logs');
    }
}