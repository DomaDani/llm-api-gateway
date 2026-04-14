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
            const message = await changeIdentity({ email, username });

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
        <form autoComplete="off" className="w-full max-w-md" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Update Profile</h2>
                    <div className="mt-3 space-y-8">
                        <AlertBox message={error} variant="error" className="mt-0" />
                        <AlertBox message={success} variant="success" className="mt-0" />

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
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
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
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="pt-6">
                        <button
                            type="submit"
                            disabled={loading || sessionExpired}
                            className={`rounded-md px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${loading || sessionExpired ? 'cursor-not-allowed bg-indigo-400' : 'cursor-pointer bg-indigo-500 hover:bg-indigo-400'}`}
                        >
                            {sessionExpired ? 'Session Expired' : loading ? 'Updating...' : 'Update'}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
