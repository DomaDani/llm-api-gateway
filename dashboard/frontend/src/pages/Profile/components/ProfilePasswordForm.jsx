import { useEffect, useState } from "react"

import { useAuth, } from "../../../api/auth/AuthProvider";
import { isTokenExpired } from "../../../api/auth/token";
import AlertBox from "../../../components/primitives/AlertBox";
import useProfilePasswordUpdate from "../../../hooks/useProfilePasswordUpdate";

/**
 * Form for updating user password with validation and expiry checks.
 *
 * @returns {JSX.Element} The rendered form.
 */
export default function ProfilePasswordForm() {
    const { user, token } = useAuth();

    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [newPasswordConfirm, setNewPasswordConfirm] = useState('');
    const sessionExpired = !token || isTokenExpired(token)
    const {
        profilePasswordError,
        profilePasswordSuccess,
        profilePasswordLoading,
        handleUpdateProfilePassword,
    } = useProfilePasswordUpdate({ sessionExpired })

    useEffect(() => {
        if (user) {
            setCurrentPassword('')
            setNewPassword('')
            setNewPasswordConfirm('')
        }
    }, [user]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const updated = await handleUpdateProfilePassword({
            currentPassword,
            newPassword,
            newPasswordConfirm,
        })

        if (updated) {
            setCurrentPassword('')
            setNewPassword('')
            setNewPasswordConfirm('')
        }
    }

    return (
        <form autoComplete="off" className="w-full max-w-md" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Change Password</h2>
                    <div className="mt-3 space-y-8">
                        <AlertBox message={profilePasswordError} variant="error" className="mt-0" />
                        <AlertBox message={profilePasswordSuccess} variant="success" className="mt-0" />

                        {/* Chrome autofill is unhinged and needs this, despite the inputs being named correctly */}
                        <input
                            type="email"
                            name="email"
                            autoComplete="username"
                            value={user?.email || ''}
                            readOnly
                            className="hidden"
                        />

                        <div>
                            <label htmlFor="profile-current-password" className="block text-sm/6 font-medium text-white">
                                Current password
                            </label>
                            <div className="mt-2">
                                <input
                                    id="profile-current-password"
                                    name="current-password"
                                    type="password"
                                    placeholder="Current password"
                                    autoComplete="current-password"
                                    required
                                    value={currentPassword}
                                    onChange={(e) => setCurrentPassword(e.target.value)}
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="profile-new-password" className="block text-sm/6 font-medium text-white">
                                New password
                            </label>
                            <div className="mt-2">
                                <input
                                    id="profile-new-password"
                                    name="new-password"
                                    type="password"
                                    placeholder="New password"
                                    autoComplete="new-password"
                                    required
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="profile-repeat-password" className="block text-sm/6 font-medium text-white">
                                Retype new password
                            </label>
                            <div className="mt-2">
                                <input
                                    id="profile-repeat-password"
                                    name="repeat-password"
                                    type="password"
                                    placeholder="Retype new password"
                                    autoComplete="new-password"
                                    required
                                    value={newPasswordConfirm}
                                    onChange={(e) => setNewPasswordConfirm(e.target.value)}
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="pt-6">
                        <button
                            type="submit"
                            disabled={profilePasswordLoading || sessionExpired}
                            className={`rounded-md px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${profilePasswordLoading || sessionExpired ? 'cursor-not-allowed bg-indigo-400' : 'cursor-pointer bg-indigo-500 hover:bg-indigo-400'}`}
                        >
                            {sessionExpired ? 'Session Expired' : profilePasswordLoading ? 'Submitting...' : 'Submit'}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
