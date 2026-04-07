export default function ProfileIdentityForm() {
    return (
        <form autoComplete="off" className="w-full max-w-md space-y-3">
            <h2 className="text-base/7 font-semibold text-white">Update Profile</h2>
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
