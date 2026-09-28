import { useAuth } from "../auth/AuthContext";

function Header() {
  const { user, isLoading } = useAuth();

  return (
    <header className="app-header">
      <h1>Bloggerrr</h1>

      <div className="header-user">
        {isLoading ? (
          <span>Loading...</span>
        ) : user ? (
          <span>{user.username}</span>
        ) : (
          <span>Guest</span>
        )}
      </div>
    </header>
  );
}

export default Header;
