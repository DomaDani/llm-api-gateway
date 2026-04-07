import { useState } from "react"
import Dropdown from "../../../components/primitives/Dropdown"

const PLACEHOLDER_USERS = [
    "User 1",
    "User 2",
    "User 3",
    "User 4",
    "User 5",
]

export default function AddUserForm({ users = PLACEHOLDER_USERS, onSubmit }) {
    const [username, setUsername] = useState("")

    function handleSubmit(event) {
        event.preventDefault()
        onSubmit?.({
            username
        })
    }

    return (
        <form autoComplete="off" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Add User</h2>
                    {/* <p className="mt-1 text-sm/6 text-gray-400">
                    </p> */}
                    <div className="mt-3 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">

                        <div className="sm:col-span-4">
                            <label htmlFor="username" className="block text-sm/6 font-medium text-white">
                                User
                            </label>
                            <div className="mt-2">
                                <Dropdown
                                    items={users}
                                    itemName="user"
                                    onSelect={setUsername}
                                    required
                                    name="username"
                                />
                            </div>
                        </div>

                    </div>
                    <div className="sm:col-span-4 pt-6">
                        <button
                            type="submit"
                            className="cursor-pointer rounded-md bg-indigo-500 px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 hover:bg-indigo-400"
                        >
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
