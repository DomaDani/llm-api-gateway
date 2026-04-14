import { useState, useEffect } from "react"
import Dropdown from "../../../components/primitives/Dropdown"
import { fetchUserInfos } from "../../../api/management/user/Info"

export default function AddUserForm({ onSubmit }) {
    const [userId, setUserId] = useState(null)
    const [availableUsers, setAvailableUsers] = useState([])
    const [userMap, setUserMap] = useState({})

    useEffect(() => {
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
                console.error("Failed to load users:", err)
            })

        return () => { mounted = false }
    }, [])

    function handleSubmit(event) {
        event.preventDefault()
        onSubmit?.({
            user_id: userId,
        })
    }

    return (
        <form autoComplete="off" className="w-full max-w-md" onSubmit={handleSubmit}>
            <div className="space-y-12">
                <div className="pb-5">
                    <h2 className="text-base/7 font-semibold text-white">Add User</h2>
                    <div className="mt-3 space-y-8">
                        <div>
                            <label htmlFor="username" className="block text-sm/6 font-medium text-white">
                                User
                            </label>
                            <div className="mt-2">
                                <Dropdown
                                    items={availableUsers}
                                    itemName="user"
                                    onSelect={(name) => {
                                        const id = userMap[name]
                                        setUserId(id ?? null)
                                    }}
                                    required
                                    name="user-id"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="pt-6">
                        <button
                            type="submit"
                            className={`rounded-md px-3 py-2 text-sm font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 bg-indigo-500 hover:bg-indigo-400`}
                        >
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        </form>
    )
}
