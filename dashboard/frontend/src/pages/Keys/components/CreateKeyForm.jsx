import InfoBox from "../../../components/primitives/InfoBox"

export default function CreateKeyForm() {
    const apiKeyValue = "placeholder-from-backend"

    return (
        <>
            <form autoComplete="off">
                <div className="space-y-12">
                    <div className="pb-5">
                        <h2 className="text-base/7 font-semibold text-white">Create New API Key</h2>
                        {/* <p className="mt-1 text-sm/6 text-gray-400">
                        </p> */}
                        <div className="mt-3 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                            <InfoBox value={apiKeyValue} className="sm:col-span-4" />
                            <div className="sm:col-span-4">
                                <label htmlFor="key-name" className="block text-sm/6 font-medium text-white">
                                    Key Name
                                </label>
                                <div className="mt-2">
                                    <input
                                        id="key-name"
                                        name="key-name"
                                        type="text"
                                        placeholder="Key Name"
                                        autoComplete="off"
                                        required
                                        className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
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
        </>
    )
}