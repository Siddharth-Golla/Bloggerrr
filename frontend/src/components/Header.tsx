import { useAuth } from "../auth/AuthContext";

function Header() {
  const { user, isLoading, logout } = useAuth();

  return (
    <header className="app-header">
      <h1>Bloggerrr</h1>

      <div className="header-user">
        {isLoading ? (
          <span>Loading...</span>
        ) : user ? (
          <div>
            <span>{user.username}</span>
            <button type="button" onClick={logout}>
              Logout
            </button>
          </div>
        ) : (
          <span>Guest</span>
        )}
      </div>
    </header>
  );
}

export default Header;
