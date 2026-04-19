import api from "../../axios";

/**
 * Make a request to change a user's password.
 *
 * @param {object} params - Password change parameters.
 * @param {string | null} params.currentPassword - Current password when changing your own password.
 * @param {string} params.newPassword - New password.
 * @param {string} params.newPasswordConfirm - Confirmation of the new password.
 * @param {number | null} params.userId - Target user identifier for admin changes.
 * @param {boolean} params.mandateReset - Whether the new password should be marked as expired.
 * @returns {Promise<string>} A promise resolving to the success message.
 */
export async function changePassword({ currentPassword = null, newPassword, newPasswordConfirm, userId = null, mandateReset = false }) {
    try {
        
        const payload = {
            new_password: newPassword,
            new_password_confirm: newPasswordConfirm,
        };

        if (currentPassword) {
            payload.current_password = currentPassword;
        }

        if (userId != null) {
            payload.user_id = userId;
        }

        if (mandateReset) {
            payload.mandate_reset = mandateReset;
        }

        const response = await api.put('/users/change-password', payload);
        return response.data?.message || 'Password updated successfully.';
    } catch (error) {
        const backendMessage = error?.response?.data?.detail

        throw new Error(backendMessage || 'Could not update password. Please try again.')
    }

}
