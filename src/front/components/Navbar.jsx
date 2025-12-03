import { Link, useNavigate } from "react-router-dom";

export const Navbar = () => {
	const navigate = useNavigate();

	const logout = () => {
		sessionStorage.removeItem("token");
		navigate("/login");
	};

	const isLogged = sessionStorage.getItem("token") !== null;

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React + Flask JWT</span>
				</Link>

				<div>
					{!isLogged ? (
						<>
							<Link to="/login" className="btn btn-outline-primary mx-2">Login</Link>
							<Link to="/signup" className="btn btn-primary">Signup</Link>
						</>
					) : (
						<button onClick={logout} className="btn btn-danger">Logout</button>
					)}
				</div>
			</div>
		</nav>
	);
};
