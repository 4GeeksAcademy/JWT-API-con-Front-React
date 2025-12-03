import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Private = () => {
    const [data, setData] = useState(null);
    const navigate = useNavigate();
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    useEffect(() => {
        const token = sessionStorage.getItem("token");

        if (!token) {
            navigate("/login");
            return;
        }

        fetch(`${backendUrl}/api/private`, {
            headers: {
                "Authorization": "Bearer " + token
            }
        })
        .then(resp => {
            if (!resp.ok) navigate("/login");
            return resp.json();
        })
        .then(data => setData(data))
        .catch(() => navigate("/login"));

    }, []);

    return (
        <div className="container mt-5">
            <h2>Private Page</h2>
            <p>Welcome!</p>

            {data && (
                <div className="alert alert-success">
                    Authenticated as: {data.user.email}
                </div>
            )}
        </div>
    );
};
