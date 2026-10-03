import { createBrowserRouter } from "react-router-dom";

import RequireAuth from "../auth/RequireAuth";
import AppLayout from "../layouts/AppLayout";
import DashboardPage from "../pages/DashboardPage";
import ProfilePage from "../pages/ProfilePage";
import PostsPage from "../pages/PostsPage";
import RoomsPage from "../pages/RoomsPage";
import AdminPage from "../pages/AdminPage";
import RegisterPage from "../pages/RegisterPage";
import LoginPage from "../pages/LoginPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        element: <RequireAuth />,
        children: [
          { index: true, element: <DashboardPage /> },
          { path: "profile", element: <ProfilePage /> },
          { path: "posts", element: <PostsPage /> },
          { path: "rooms", element: <RoomsPage /> },
          { path: "admin", element: <AdminPage /> },
        ],
      },
      { path: "login", element: <LoginPage /> },
      { path: "register", element: <RegisterPage /> },
    ],
  },
]);