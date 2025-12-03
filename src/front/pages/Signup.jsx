import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const Signup = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const navigate = useNavigate();
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    const handleSubmit = async (e) => {
        e.preventDefault();

        const resp = await fetch(`${backendUrl}/api/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (resp.ok) {
            alert("User created successfully");
            navigate("/login");
        } else {
            alert("Error creating user");
        }
    };

    return (
        <div className="container mt-5">
            <h2>Signup</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    className="form-control mb-3"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    className="form-control mb-3"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button className="btn btn-primary">Create account</button>
            </form>
        </div>
    );
};
