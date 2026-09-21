import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="app-sidebar">
      <nav>
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/profile">Profile</NavLink>
        <NavLink to="/posts">Posts</NavLink>
        <NavLink to="/rooms">Rooms</NavLink>
        <NavLink to="/admin">Admin</NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;