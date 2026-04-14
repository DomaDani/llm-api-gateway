import api from '../axios'

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
