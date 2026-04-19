import api from "../axios";

/**
 * Fetch usage logs with optional filtering and aggregation.
 *
 * @param {number | null} projectId - Project identifier.
 * @param {number | null} userId - User identifier.
 * @param {boolean} aggregate - Whether to return aggregated rows.
 * @param {number | null} limit - Maximum number of rows to return.
 * @param {number} offset - Number of rows to skip.
 * @returns {Promise<any[]>} A promise resolving to the usage log list.
 */
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