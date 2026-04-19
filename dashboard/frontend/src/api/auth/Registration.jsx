import api from '../axios'

/**
 * Make a registration request to the backend API with the provided user details.
 * If the registration is successful, returns a success message.
 * If there is an error during registration, throws an error with a message from the backend or a generic error message.
 * @param {Object} param - The user registration parameters.
 * @param {string} param.username - The user's username.
 * @param {string} param.email - The user's email address.
 * @param {string} param.password - The user's password.
 * @param {boolean} param.mandateReset - Whether to mandate a password reset.
 * @returns {Promise<string>} A promise resolving to the registration message.
 */
export async function registerUser({ username, email, password, mandateReset }) {
	try {
		const response = await api.post('/auth/register', {
			username,
			email,
			password,
			mandate_reset: mandateReset
		})

		return response.data?.message || 'User created successfully.'
	} catch (error) {
		const backendMessage = error?.response?.data?.detail

		throw new Error(backendMessage || 'Could not create user. Please try again.')
	}
}
