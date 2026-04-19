import ProfileIdentityForm from "./components/ProfileIdentityForm"
import ProfilePasswordForm from "./components/ProfilePasswordForm"
import { useAuth } from "../../api/auth/AuthProvider"
import AlertBox from "../../components/primitives/AlertBox"

/**
 * User profile page for managing account identity, password, and settings.
 *
 * @returns {JSX.Element} The rendered profile page.
 */
export default function Profile() {
    const { user } = useAuth()
    return (
        <div className="flex flex-col gap-8">
            <h1 className="shrink-0 text-3xl font-bold text-white">Profile</h1>
            <div className="border-b border-white/10 pb-5">
                <ProfileIdentityForm />
            </div>
            <div className="border-b border-white/10 pb-5">
                {user?.is_password_expired && (
                    <AlertBox message={"Your password has expired — please update it below."} variant="warning" className="mt-0" />
                )}
                <ProfilePasswordForm />
            </div>
        </div>
    )
}