import api from '../axios'

export async function registerUser({ username, email, password, mandateReset }) {
	try {
		const response = await api.post('/auth/register', {
			username,
			email,
			password,
            mandateReset
		})

		return response.data?.message || 'User created successfully.'
	} catch (err) {
		const backendMessage = err?.response?.data?.detail
		const normalizedMessage = Array.isArray(backendMessage)
			? backendMessage.map((issue) => issue.msg).join(', ')
			: backendMessage

		throw new Error(normalizedMessage || 'Could not create user. Please try again.')
	}
}
