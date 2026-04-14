import api from "../../axios";

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
