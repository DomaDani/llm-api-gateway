import { useAuth } from "../../auth/AuthProvider";

export default function Welcome() {
    const { logout, user } = useAuth();

    return (
        <>
            <div className="flex min-h-screen flex-col items-center justify-center bg-gray-900 text-white">
                <h1 className="mt-10 text-center text-5xl/9 font-bold tracking-tight text-white">Welcome, {user.username}!</h1>
            
            <div className="mt-10 flex items-center justify-center gap-x-6">
                    <button
                        onClick={logout}
                        className="rounded-md bg-red-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600"
                    >
                        Sign out
                    </button>
            </div>
            
            </div>

        </>
    );
}