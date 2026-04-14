import { useEffect, useState } from 'react'

import Dropdown from '../../../components/primitives/Dropdown'
import { fetchUserInfos } from '../../../api/management/user/Info'
import { changePassword } from '../../../api/management/user/ChangePassword'
import { useAuth } from '../../../api/auth/AuthProvider'
import { isTokenExpired } from '../../../api/auth/token'
import AlertBox from '../../../components/primitives/AlertBox'

export default function SetUserPasswordForm() {
    const { token } = useAuth()

    const [availableUsers, setAvailableUsers] = useState([])
    const [userMap, setUserMap] = useState({})
    const [selectedUserId, setSelectedUserId] = useState(null)
    const [password, setPassword] = useState('')
    const [mandateReset, setMandateReset] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')
    const [loading, setLoading] = useState(false)

    const sessionExpired = !token || isTokenExpired(token)

    useEffect(() => {
        if (sessionExpired) {
            setError('Your session has expired. Please sign in again.')
            return
        }

        let mounted = true

        fetchUserInfos()
            .then((data) => {
                if (!mounted) return
                if (Array.isArray(data) && data.length > 0) {
                    const names = data.map((u) => u.username)
                    const map = data.reduce((acc, u) => { acc[u.username] = u.id; return acc }, {})
                    setAvailableUsers(names)
                    setUserMap(map)
                } else {
                    setAvailableUsers([])
                    setUserMap({})
                }
            })
            .catch((err) => {
                setError(err.message || 'Failed to load users.')
            })

        return () => { mounted = false }
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
            const message = await changePassword({
                userId: selectedUserId ? Number(selectedUserId) : null,
                newPassword: password,
                newPasswordConfirm: password,
                mandateReset
            })

            setSuccess(message)
            setPassword('')
            setMandateReset(false)
        } catch (err) {
            setError(err.message || 'Could not update password. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <form autoComplete="off" className="w-full max-w-md" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Set User Password</h2>
                    <div className="mt-3 space-y-8">
                        <AlertBox message={error} variant="error" className="mt-0" />
                        <AlertBox message={success} variant="success" className="mt-0" />

                        <div>
                            <label htmlFor="user-id" className="block text-sm/6 font-medium text-white">
                                User
                            </label>
                            <div className="mt-2">
                                <Dropdown
                                    items={availableUsers}
                                    itemName="user"
                                    onSelect={(name) => {
                                        const id = userMap[name]
                                        setSelectedUserId(id ?? null)
                                    }}
                                    required
                                    name="user-id"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="new-password" className="block text-sm/6 font-medium text-white">
                                New password
                            </label>
                            <div className="mt-2">
                                <input
                                    id="new-password"
                                    name="new-password"
                                    type="password"
                                    placeholder="New password"
                                    autoComplete="new-password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
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
                                        Upon their next log-in, the user will be forced to create a new password.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="pt-6">
                        <button
                            type="submit"
                            disabled={loading || sessionExpired}
                            className={`rounded-md px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${loading || sessionExpired ? 'cursor-not-allowed bg-indigo-400' : 'cursor-pointer bg-indigo-500 hover:bg-indigo-400'}`}
                        >
                            {sessionExpired ? 'Session expired' : loading ? 'Updating...' : 'Submit'}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
