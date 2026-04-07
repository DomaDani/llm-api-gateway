export default function ProfilePasswordForm() {
    return (
        <form autoComplete="off" className="w-full max-w-md space-y-3">
            <h2 className="text-base/7 font-semibold text-white">Change Password</h2>
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
                        className="block w-full rounded-md bg-white/5 px-3 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
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
                        className="block w-full rounded-md bg-white/5 px-3 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
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
                        className="block w-full rounded-md bg-white/5 px-3 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
                    />
                </div>
            </div>

            <button
                type="submit"
                className="cursor-pointer rounded-md bg-indigo-500 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
                Submit
            </button>
        </form>
    )
}
