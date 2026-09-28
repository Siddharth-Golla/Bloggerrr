import { useState } from "react";
import type { SubmitEvent } from "react";
import { Link } from "react-router-dom";

import { registerUser } from "../services/api";

function RegisterPage() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    async function handleSubmit(
        event: SubmitEvent<HTMLFormElement>,
    ) {
        event.preventDefault();

        setMessage("");
        setError("");
        setIsSubmitting(true);

        try {
            const user = await registerUser({
                username,
                email,
                password,
            });

            setMessage(`User ${user.username} registered successfully.`);

            setUsername("");
            setEmail("");
            setPassword("");
        } catch (error) {
            setError(
                error instanceof Error
                    ? error.message
                    : "Registration failed",
            );
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <section>
            <h2>Create an account</h2>

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username</label>
                    <input
                        id="username"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                        required
                    />
                </div>

                <div>
                    <label htmlFor="email">Email</label>
                    <input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        required
                    />
                </div>

                <div>
                    <label htmlFor="password">Password</label>
                    <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                    />
                </div>

                <button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Registering..." : "Register"}
                </button>
            </form>

            {message && <p>{message}</p>}
            {error && <p role="alert">{error}</p>}

            <p>
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </section>
    );
}

export default RegisterPage;