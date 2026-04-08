import api from "../../axios";

export async function changePassword({ currentPassword, newPassword, newPasswordConfirm }) {
    try {
        const response = await api.put('/users/change-password', {
            current_password: currentPassword,
            new_password: newPassword,
            new_password_confirm: newPasswordConfirm
        });
        return response.data?.message || 'Password updated successfully.';
    } catch (error) {
        const backendMessage = error?.response?.data?.detail

        throw new Error(backendMessage || 'Could not update password. Please try again.')
    }

}
