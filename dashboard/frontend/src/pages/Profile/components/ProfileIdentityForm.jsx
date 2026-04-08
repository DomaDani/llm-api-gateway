import { useEffect, useState } from "react"

import { changeIdentity } from "../../../api/management/user/ChangeIdentity";
import { useAuth, } from "../../../api/auth/AuthProvider";
import { isTokenExpired } from "../../../api/auth/token";
import AlertBox from "../../../components/primitives/AlertBox";

export default function ProfileIdentityForm() {
    const { user, token } = useAuth();

    const [username, setUsername] = useState(user?.username || '');
    const [email, setEmail] = useState(user?.email || '');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);

    const sessionExpired = !token || isTokenExpired(token)

    useEffect(() => {
        if (sessionExpired) {
            setError("Your session has expired. Please sign in again.")
        }
    }, [sessionExpired])

    useEffect(() => {
        if (user) {
            setUsername(user.username);
            setEmail(user.email);
        }
    }, [user]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (sessionExpired) {
            setError("Your session has expired. Please sign in again.")
            return
        }

        setError('');
        setSuccess('');
        setLoading(true);

        try {
            const message = await changeIdentity({ id: user.id, email, username });

            setSuccess(message)
            setUsername(username)
            setEmail(email)
        } catch (error) {
            setError(error.message || 'Failed to update identity.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <form autoComplete="off" className="w-full max-w-md space-y-3" onSubmit={handleSubmit}>
            <h2 className="text-base/7 font-semibold text-white">Update Profile</h2>

            <AlertBox message={error} variant="error" />
            <AlertBox message={success} variant="success" />

            <div>
                <label htmlFor="profile-username" className="block text-sm/6 font-medium text-white">
                    Username
                </label>
                <div className="mt-2">
                    <input
                        id="profile-username"
                        name="username"
                        type="text"
                        placeholder="Username"
                        autoComplete="off"
                        required
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="block w-full rounded-md bg-white/5 px-3 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
                    />
                </div>
            </div>
            <div>
                <label htmlFor="profile-email" className="block text-sm/6 font-medium text-white">
                    Email address
                </label>
                <div className="mt-2">
                    <input
                        id="profile-email"
                        name="email"
                        type="email"
                        placeholder="Email address"
                        autoComplete="off"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="block w-full rounded-md bg-white/5 px-3 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
                    />
                </div>
            </div>

            <button
                type="submit"
                disabled={loading || sessionExpired}
                className="cursor-pointer rounded-md bg-indigo-500 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
                {sessionExpired ? 'Session Expired' : loading ? 'Updating...' : 'Update'}
            </button>
        </form>
    )
}
