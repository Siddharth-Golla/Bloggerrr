import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "./AuthContext";

function RequireAuth() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <p>Checking authentication...</p>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}

export default RequireAuth;