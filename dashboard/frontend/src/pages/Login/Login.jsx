import LoginForm from "./components/LoginForm";

/**
 * Login page for unauthenticated users to sign in.
 *
 * @returns {JSX.Element} The rendered login page.
 */
export default function Login() {
    return (
        <>
            <div>
                <LoginForm />
            </div>
        </>
    );
}