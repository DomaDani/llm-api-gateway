import { useEffect, useState } from 'react'

import { registerUser } from '../../../api/auth/Registration'
import { useAuth } from '../../../api/auth/AuthProvider'
import { isTokenExpired } from '../../../api/auth/token'

export default function CreateUserForm() {
    const { token } = useAuth()

    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [mandateReset, setMandateReset] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')
    const [loading, setLoading] = useState(false)

    const sessionExpired = !token || isTokenExpired(token)

    useEffect(() => {
        if (sessionExpired) {
            setError('Your session has expired. Please sign in again.')
        }
    }, [sessionExpired])

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (sessionExpired) {
            setError('Your session has expired. Please sign in again.')
            return
        }

        setError('')
        setSuccess('')
        setLoading(true)

        try {
            const message = await registerUser({
                username,
                email,
                password,
                mandateReset
            })

            setSuccess(message)
            setUsername('')
            setEmail('')
            setPassword('')
            setMandateReset(false)
        } catch (err) {
            setError(err.message || 'Could not create user. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <form autoComplete="off" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Create New User</h2>
                    {/* <p className="mt-1 text-sm/6 text-gray-400">
                    </p> */}

                    {error && (
                        <div className="mt-3 rounded border border-red-500/50 bg-red-500/10 p-2 text-sm text-red-300">
                            {error}
                        </div>
                    )}

                    {success && (
                        <div className="mt-3 rounded border border-emerald-500/50 bg-emerald-500/10 p-2 text-sm text-emerald-300">
                            {success}
                        </div>
                    )}

                    <div className="mt-3 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                        <div className="sm:col-span-4">
                            <label htmlFor="username" className="block text-sm/6 font-medium text-white">
                                Username
                            </label>
                            <div className="mt-2">
                                <input
                                    id="username"
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

                        <div className="sm:col-span-4">
                            <label htmlFor="email" className="block text-sm/6 font-medium text-white">
                                Email address
                            </label>
                            <div className="mt-2">
                                <input
                                    id="email"
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

                        <div className="sm:col-span-4">
                            <label htmlFor="password" className="block text-sm/6 font-medium text-white">
                                Password
                            </label>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    placeholder="Password"
                                    autoComplete="off"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <div className="flex gap-3">
                                <div className="flex h-6 shrink-0 items-center">
                                    <div className="group grid size-4 grid-cols-1">
                                        <input
                                            id="pw-reset"
                                            name="pw-reset"
                                            type="checkbox"
                                            aria-describedby="pw-reset-description"
                                            checked={mandateReset}
                                            onChange={(e) => setMandateReset(e.target.checked)}
                                            className="col-start-1 row-start-1 appearance-none rounded-sm border border-white/10 bg-white/5 checked:border-indigo-500 checked:bg-indigo-500 indeterminate:border-indigo-500 indeterminate:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:border-white/5 disabled:bg-white/10 disabled:checked:bg-white/10 forced-colors:appearance-auto"
                                        />
                                        <svg
                                            fill="none"
                                            viewBox="0 0 14 14"
                                            className="pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white group-has-disabled:stroke-white/25"
                                        >
                                            <path
                                                d="M3 8L6 11L11 3.5"
                                                strokeWidth={2}
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                className="opacity-0 group-has-checked:opacity-100"
                                            />
                                            <path
                                                d="M3 7H11"
                                                strokeWidth={2}
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                className="opacity-0 group-has-indeterminate:opacity-100"
                                            />
                                        </svg>
                                    </div>
                                </div>
                                <div className="text-sm/6">
                                    <label htmlFor="pw-reset" className="font-medium text-white">
                                        Mandate password reset?
                                    </label>
                                    <p id="pw-reset-description" className="text-gray-400">
                                        Upon their first log-in, the user will be forced to create a new password.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="sm:col-span-4 pt-6">
                        <button
                            type="submit"
                            disabled={loading || sessionExpired}
                            className={`rounded-md px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${loading || sessionExpired ? 'cursor-not-allowed bg-indigo-400' : 'cursor-pointer bg-indigo-500 hover:bg-indigo-400'}`}
                        >
                            {sessionExpired ? 'Session expired' : loading ? 'Creating user...' : 'Submit'}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
